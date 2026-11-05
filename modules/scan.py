import socket
import subprocess

NAME = "/scan"
DESC = "varre rede Wi-Fi: /scan [portas] (padrao: comuns)"

VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
CIANO = "\033[96m"
CINZA = "\033[90m"
NEGRITO = "\033[1m"
RESET = "\033[0m"

PORTAS_COMUNS = [21, 22, 23, 53, 80, 443, 445, 8080, 8443, 3389]
TIMEOUT_PING = 1
TIMEOUT_PORTA = 0.5


def _ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


def _ping(ip):
    try:
        p = subprocess.run(
            ["ping", "-c", "1", "-W", str(TIMEOUT_PING), ip],
            capture_output=True,
            timeout=TIMEOUT_PING + 2,
            stdin=subprocess.DEVNULL,
        )
        return p.returncode == 0
    except Exception:
        return False


def _porta_aberta(ip, porta):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT_PORTA)
        r = s.connect_ex((ip, porta))
        s.close()
        return r == 0
    except Exception:
        return False


def run(shell, args):
    ip_local = _ip_local()
    if not ip_local:
        shell.socket.send(
            f"{VERMELHO}erro: nao consegui detectar IP local (wifi desligado?){RESET}\n".encode()
        )
        return

    base = ".".join(ip_local.split(".")[:3])
    shell.socket.send(
        f"{CIANO}{NEGRITO}[scan]{RESET} ip local: {AMARELO}{ip_local}{RESET}\n"
        f"{CINZA}varrendo {base}.1-254...{RESET}\n".encode()
    )

    portas = PORTAS_COMUNS
    if args.strip():
        try:
            portas = [int(p) for p in args.strip().split(",")]
        except ValueError:
            shell.socket.send(b"uso: /scan [porta1,porta2,...]\n")
            return

    encontrados = []
    for i in range(1, 255):
        ip = f"{base}.{i}"
        if _ping(ip):
            encontrados.append(ip)

    if not encontrados:
        shell.socket.send(f"{VERMELHO}nenhum host respondeu ao ping{RESET}\n".encode())
        return

    shell.socket.send(
        f"{VERDE}hosts ativos: {len(encontrados)}{RESET}\n"
        f"{CINZA}testando portas...{RESET}\n".encode()
    )

    linhas = [
        f"{CIANO}{NEGRITO}{'IP':<16} {'PORTAS ABERTAS'}{RESET}",
        f"{CIANO}{'-'*50}{RESET}",
    ]

    for ip in encontrados:
        abertas = []
        for p in portas:
            if _porta_aberta(ip, p):
                abertas.append(str(p))

        if abertas:
            portas_txt = f"{VERDE}{','.join(abertas)}{RESET}"
        else:
            portas_txt = f"{CINZA}-{RESET}"
        linhas.append(f"{AMARELO}{ip:<16}{RESET} {portas_txt}")
    linhas.append(f"\n{CINZA}total: {len(encontrados)} host(s){RESET}")
    shell.socket.send(("\n".join(linhas) + "\n").encode())
