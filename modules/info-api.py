import subprocess

NAME = "/info-api"
DESC = "info do aparelho: /info sensor|device|cell [args]"


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
        shell.socket.send(b"uso: /info sensor|device|cell [args]\n")
        return

    sub = partes[0].lower()
    resto = partes[1] if len(partes) > 1 else ""

    if sub == "sensor":
        _sensor(shell, resto)
    elif sub == "device":
        _device(shell)
    elif sub == "cell":
        _cell(shell)
    else:
        shell.socket.send(f"subcomando desconhecido: {sub}\n".encode())


def _sensor(shell, args):
    alvo = args.strip()
    if not alvo or alvo.lower() == "list":
        rc, out, err = _run(["termux-sensor", "-l"])
        if rc == 0:
            shell.socket.send((out + "\n").encode())
        else:
            shell.socket.send(f"erro: {err or out or rc}\n".encode())
        return

    rc, out, err = _run(
        ["termux-sensor", "-s", alvo, "-n", "1"],
        timeout=20,
    )
    if rc == 0:
        shell.socket.send((out + "\n").encode())
    else:
        shell.socket.send(f"erro: {err or out or rc}\n".encode())


def _device(shell):
    rc, out, err = _run(["termux-telephony-deviceinfo"])
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
