import time
import requests
import shutil
import subprocess
from stem import Signal
from stem.control import Controller
from brute import force



TOR_PROXY = {
    "http": "socks5h://127.0.0.1:9050", # h = hostname resolution through proxy (DNS)
    "https": "socks5h://127.0.0.1:9050",
}

CONTROL_PORT = 9051

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


def run_actions_with_rotation(actions_per_ip: int = 5) -> None:
    """
    Beispiel-Logik:
    Nach X Aktionen wird eine neue Tor-IP angefordert.
    """
    counter = 0

    while True:
        ip = get_current_ip()
        print(f"[+] Current Tor IP: {ip}")

        # Hier kommt deine erlaubte Aktion rein
        print("[*] Doing action...")




        force.fire() # brute force with hydra




        

        counter += 1

        if counter >= actions_per_ip:
            print("[*] Rotating Tor IP...")
            rotate_tor_ip()
            counter = 0

            # Tor ignoriert zu schnelle NEWNYM-Anfragen oft.
            # 10 Sekunden ist realistischer als 3 Sekunden.
            time.sleep(10)

        time.sleep(1)


if __name__ == "__main__":
    start_tor_if_needed()
    run_actions_with_rotation(actions_per_ip=5)