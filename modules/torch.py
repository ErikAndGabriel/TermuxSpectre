import subprocess
import time

NAME = "/torch"
DESC = "lanterna: /torch on|off|blink|status"


def _run(args_list):
    try:
        p = subprocess.run(
            ["termux-torch", *args_list],
            capture_output=True,
            text=True,
            timeout=10,
            stdin=subprocess.DEVNULL,
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except FileNotFoundError:
        return -1, "", "termux-torch nao instalado"
    except subprocess.TimeoutExpired:
        return -2, "", "timeout"
    except Exception as e:
        return -3, "", str(e)


def run(shell, args):
    action = args.strip().lower() or "status"

    if action in ("on", "ligar", "1"):
        rc, out, err = _run(["on"])
        if rc == 0:
            shell.socket.send(b"lanterna: ON\n")
        else:
            shell.socket.send(f"erro: {err or out or rc}\n".encode())

    elif action in ("off", "desligar", "0"):
        rc, out, err = _run(["off"])
        if rc == 0:
            shell.socket.send(b"lanterna: OFF\n")
        else:
            shell.socket.send(f"erro: {err or out or rc}\n".encode())

    elif action in ("blink", "piscar"):
        try:
            for _ in range(6):
                _run(["on"])
                time.sleep(0.3)
                _run(["off"])
                time.sleep(0.3)
            shell.socket.send(b"lanterna: blink ok\n")
        except Exception as e:
            shell.socket.send(f"erro: {e}\n".encode())

    elif action in ("status", "estado"):
        rc, out, err = _run(["status"])
        if rc == 0 and out:
            shell.socket.send(f"lanterna: {out}\n".encode())
        else:
            shell.socket.send(b"lanterna: status nao suportado neste aparelho\n")

    else:
        shell.socket.send(b"uso: /torch on|off|blink|status\n")
