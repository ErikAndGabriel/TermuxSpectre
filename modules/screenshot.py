import os
import subprocess
import time

NAME = "/screenshot"
DESC = "captura de tela e envia (PNG)"


def run(shell, args):
    nome = f"screen_{int(time.time())}.png"
    path = f"/data/data/com.termux/files/usr/tmp/{nome}"

    try:
        if os.path.exists(path):
            os.remove(path)

        p = subprocess.run(
            ["screencap", "-p", path],
            capture_output=True, text=True,
            timeout=15, stdin=subprocess.DEVNULL,
        )

        if p.returncode != 0 or not os.path.exists(path):
            msg = (p.stderr or p.stdout or f"exit {p.returncode}").strip()
            shell.socket.send(f"erro: {msg}\n".encode())
            return

        size = os.path.getsize(path)
        if size == 0:
            shell.socket.send(b"erro: captura vazia\n")
            return

        shell.socket.sendall(f"FILE {nome} {size}\n".encode())

        enviado = 0
        with open(path, "rb") as f:
            while enviado < size:
                chunk = f.read(65536)
                if not chunk:
                    break
                shell.socket.sendall(chunk)
                enviado += len(chunk)

        shell.socket.sendall(b"\n")
        os.remove(path)

    except FileNotFoundError:
        shell.socket.send(b"erro: screencap nao encontrado\n")
    except subprocess.TimeoutExpired:
        shell.socket.send(b"erro: timeout (tela protegida?)\n")
    except Exception as e:
        shell.socket.send(f"erro: {e}\n".encode())
