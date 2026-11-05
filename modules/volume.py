import subprocess

NAME = "/volume"
DESC = "volume: /volume (lista) | /volume <stream> <0-15>"


def run(shell, args):
    partes = args.strip().split(None, 1)
    try:
        if not partes:
            p = subprocess.run(
                ["termux-volume"],
                capture_output=True, text=True, timeout=10,
                stdin=subprocess.DEVNULL,
            )
            if p.returncode == 0:
                shell.socket.send((p.stdout.strip() + "\n").encode())
            else:
                shell.socket.send(f"erro: {p.stderr or p.returncode}\n".encode())
            return
        if len(partes) != 2:
            shell.socket.send(b"uso: /volume <stream> <0-15>\nstreams: music ring notification alarm call system\n")
            return
        stream = partes[0].lower()
        try:
            valor = int(partes[1])
        except ValueError:
            shell.socket.send(b"erro: valor deve ser numero 0-15\n")
            return
        p = subprocess.run(
            ["termux-volume", stream, str(valor)],
            capture_output=True, text=True, timeout=10,
            stdin=subprocess.DEVNULL,
        )
        if p.returncode == 0:
            shell.socket.send(f"volume {stream} = {valor}\n".encode())
        else:
            shell.socket.send(f"erro: {p.stderr or p.stdout or p.returncode}\n".encode())
    except FileNotFoundError:
        shell.socket.send(b"erro: termux-volume nao instalado\n")
    except subprocess.TimeoutExpired:
        shell.socket.send(b"erro: timeout\n")
    except Exception as e:
        shell.socket.send(f"erro: {e}\n".encode())
