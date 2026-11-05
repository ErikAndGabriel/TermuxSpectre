import subprocess

NAME = "/phone"
DESC = "telefone: /phone call|sms|contacts|logs|inbox|cell"


def _run(args_list, timeout=15):
    try:
        p = subprocess.run(
            args_list,
            capture_output=True,
            text=True,
            timeout=timeout,
            stdin=subprocess.DEVNULL,
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except FileNotFoundError:
        return -1, "", f"{args_list[0]} nao instalado"
    except subprocess.TimeoutExpired:
        return -2, "", "timeout"
    except Exception as e:
        return -3, "", str(e)


def run(shell, args):
    partes = args.strip().split(None, 1)
    if not partes:
        shell.socket.send(b"uso: /phone call|sms|contacts|logs|inbox|cell\n")
        return

    sub = partes[0].lower()
    resto = partes[1] if len(partes) > 1 else ""

    if sub == "call":
        _call(shell, resto)
    elif sub == "sms":
        _sms(shell, resto)
    elif sub == "contacts":
        _contacts(shell)
    elif sub == "logs":
        _logs(shell, resto)
    elif sub == "inbox":
        _inbox(shell, resto)
    elif sub == "cell":
        _cell(shell)
    else:
        shell.socket.send(f"subcomando desconhecido: {sub}\n".encode())


def _call(shell, numero):
    numero = numero.strip()
    if not numero:
        shell.socket.send(b"uso: /phone call <numero>\n")
        return
    rc, out, err = _run(["termux-telephony-call", numero])
    if rc == 0:
        shell.socket.send(f"chamando {numero}\n".encode())
    else:
        shell.socket.send(f"erro: {err or out or rc}\n".encode())


def _sms(shell, args):
    partes = args.split(None, 1)
    if len(partes) != 2:
        shell.socket.send(b"uso: /phone sms <numero> <texto>\n")
        return
    numero, texto = partes
    rc, out, err = _run(["termux-sms-send", "-n", numero, texto])
    if rc == 0:
        shell.socket.send(f"sms enviado para {numero}\n".encode())
    else:
        shell.socket.send(f"erro: {err or out or rc}\n".encode())


def _contacts(shell):
    rc, out, err = _run(["termux-contact-list"])
    if rc == 0:
        shell.socket.send((out + "\n").encode())
    else:
        shell.socket.send(f"erro: {err or rc}\n".encode())


def _logs(shell, args):
    limite = args.strip() or "10"
    try:
        int(limite)
    except ValueError:
        shell.socket.send(b"uso: /phone logs [limite]\n")
        return
    rc, out, err = _run(["termux-call-log", "-l", limite])
    if rc == 0:
        shell.socket.send((out + "\n").encode())
    else:
        shell.socket.send(f"erro: {err or rc}\n".encode())


def _inbox(shell, args):
    limite = args.strip() or "10"
    try:
        int(limite)
    except ValueError:
        shell.socket.send(b"uso: /phone inbox [limite]\n")
        return
    rc, out, err = _run(["termux-sms-list", "-l", limite, "-n", "-d"])
    if rc == 0:
        shell.socket.send((out + "\n").encode())
    else:
        shell.socket.send(f"erro: {err or out or rc}\n".encode())


def _cell(shell):
    rc, out, err = _run(["termux-telephony-cellinfo"])
    if rc == 0:
        shell.socket.send((out + "\n").encode())
    else:
        shell.socket.send(f"erro: {err or out or rc}\n".encode())
