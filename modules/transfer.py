import os
import subprocess

NAME = "/transfer"
DESC = "transferencia: /transfer up <arq> | down <url> <destino>"


def _run(args_list, timeout=60):
    try:
        p = subprocess.run(
            args_list, capture_output=True, text=True,
            timeout=timeout, stdin=subprocess.DEVNULL,
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except FileNotFoundError:
        return -1, "", f"{args_list[0]} nao instalado"
    except subprocess.TimeoutExpired:
        return -2, "", "timeout"
    except Exception as e:
        return -3, "", str(e)


def run(shell, args):
    partes = args.strip().split(None, 2)
    if len(partes) < 2:
        shell.socket.send(b"uso: /transfer up <arq> | down <url> <destino>\n")
        return

    sub = partes[0].lower()

    if sub == "up":
        _up(shell, partes[1])
    elif sub == "down":
        if len(partes) < 3:
            shell.socket.send(b"uso: /transfer down <url> <destino>\n")
            return
        _down(shell, partes[1], partes[2])
    else:
        shell.socket.send(f"subcomando desconhecido: {sub}\n".encode())


def _up(shell, caminho):
    if not os.path.isfile(caminho):
        shell.socket.send(f"erro: {caminho} nao existe\n".encode())
        return

    try:
        size = os.path.getsize(caminho)
        if size == 0:
            shell.socket.send(b"erro: arquivo vazio\n")
            return

        nome = os.path.basename(caminho)
        shell.socket.sendall(f"FILE {nome} {size}\n".encode())

        enviado = 0
        with open(caminho, "rb") as f:
            while enviado < size:
                chunk = f.read(65536)
                if not chunk:
                    break
                shell.socket.sendall(chunk)
                enviado += len(chunk)

        shell.socket.sendall(b"\n")
        shell.socket.send(f"enviado: {nome} ({size} bytes)\n".encode())

    except PermissionError:
        shell.socket.send(b"erro: sem permissao de leitura\n")
    except Exception as e:
        shell.socket.send(f"erro: {e}\n".encode())


def _down(shell, url, destino):
    destino = os.path.expanduser(destino)

    if os.path.isdir(destino):
        destino = os.path.join(destino, os.path.basename(url.split("?")[0]) or "arquivo")

    try:
        if os.path.exists(destino):
            os.remove(destino)

        shell.socket.send(f"baixando {url}...\n".encode())

        rc, out, err = _run(
            ["curl", "-fsSL", "--max-time", "120", "-o", destino, url],
            timeout=130,
        )

        if rc != 0 or not os.path.exists(destino):
            msg = err or out or f"exit {rc}"
            shell.socket.send(f"erro: {msg}\n".encode())
            return

        size = os.path.getsize(destino)
        shell.socket.send(
            f"ok: {os.path.basename(destino)} ({size} bytes)\n".encode()
        )

    except Exception as e:
        shell.socket.send(f"erro: {e}\n".encode())
