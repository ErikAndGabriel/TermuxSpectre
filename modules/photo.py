import os
import subprocess

NAME = "/photo"
DESC = "tira foto com a camera e envia (JPEG)"

CAM = "/data/data/com.termux/files/home/storage/dcim/Camera"

def run(shell, args):
    path = "/data/data/com.termux/files/usr/tmp/shot.jpg"

    try:
        if os.path.exists(path):
            os.remove(path)

        cmd = subprocess.run(
            [
                "termux-camera-photo",
                "-c", "0",
                path,
            ],
            capture_output=True,
            text=True,
            timeout=20,
            stdin=subprocess.DEVNULL,
        )

        if cmd.returncode != 0 or not os.path.exists(path):
            msg = cmd.stderr or cmd.stdout or f"exit {cmd.returncode}"
            shell.socket.send(f"erro: {msg}\n".encode())
            return

        size = os.path.getsize(path)
        if size == 0:
            shell.socket.send(b"erro: foto vazia\n")
            return

        header = f"FILE {os.path.basename(path)} {size}\n"
        shell.socket.send(header.encode())

        with open(path, "rb") as f:
            enviado = 0
            while enviado < size:
                chunk = f.read(8192)
                if not chunk:
                    break
                shell.socket.sendall(chunk)
                enviado += len(chunk)

        shell.socket.send(b"\n")
        os.remove(path)

    except FileNotFoundError:
        shell.socket.send(b"erro: termux-camera-photo nao instalado\n")
    except subprocess.TimeoutExpired:
        shell.socket.send(b"erro: timeout (camera lenta ou sem permissao)\n")
    except Exception as e:
        shell.socket.send(f"erro: {e}\n".encode())
