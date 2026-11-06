import socket
import subprocess
from config.fingerprints import (
    inferir, servicos, classificar, portas_para_scan,
)

NAME = "/scan"
DESC = "varre rede Wi-Fi com fingerprint: /scan [portas]"

VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
CIANO = "\033[96m"
MAGENTA = "\033[95m"
CINZA = "\033[90m"
NEGRITO = "\033[1m"
RESET = "\033[0m"

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


def _cor_confianca(confianca):
    return {
        "certeza": VERDE,
        "alta": VERDE,
        "media": AMARELO,
        "baixa": CINZA,
    }.get(confianca, CINZA)


def _formatar_categorias(grupos):
    partes = []
    for categoria, portas in grupos.items():
        if categoria == "?":
            continue
        partes.append(f"{categoria}: {portas}")
    return " | ".join(partes) if partes else "?"


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

    portas = portas_para_scan()
    if args.strip():
        try:
            portas = [int(p) for p in args.strip().split(",")]
        except ValueError:
            shell.socket.send(b"uso: /scan [porta1,porta2,...]\n")
            return

    shell.socket.send(
        f"{CINZA}testando {len(portas)} portas...{RESET}\n".encode()
    )

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
        f"{CINZA}testando portas e fingerprint...{RESET}\n".encode()
    )

    com_portas = 0
    for ip in encontrados:
        abertas = [p for p in portas if _porta_aberta(ip, p)]
        if not abertas:
            continue

        com_portas += 1
        info = inferir(abertas)
        servs = servicos(abertas)
        grupos = classificar(abertas)
        cats = _formatar_categorias(grupos)
        cor = _cor_confianca(info["confianca"])
        suspeito = "SUSPEITO" in info["dispositivo"]
        cor_ip = MAGENTA if suspeito else AMARELO

        shell.socket.send(
            f"\n{cor_ip}{NEGRITO}{ip}{RESET}\n"
            f"  dispositivo : {cor}{info['dispositivo']}{RESET} "
            f"{CINZA}({info['confianca']}){RESET}\n"
            f"  motivo      : {CINZA}{info['motivo']}{RESET}\n"
            f"  portas      : {VERDE}{abertas}{RESET}\n"
            f"  servicos    : {CINZA}{', '.join(servs)}{RESET}\n"
            f"  categorias  : {CINZA}{cats}{RESET}\n".encode()
        )

    if com_portas == 0:
        shell.socket.send(b"nenhum host com portas abertas\n")
    else:
        shell.socket.send(
            f"\n{CINZA}scan concluido: {com_portas} host(s) com portas abertas{RESET}\n".encode()
    )
