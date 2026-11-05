import subprocess

NAME = "/bright"
DESC = "brilho da tela: /bright [0-255]"


def run(shell, args):
    arg = args.strip()
    try:
        if not arg:
            p = subprocess.run(
                ["termux-brightness"],
                capture_output=True, text=True, timeout=10,
                stdin=subprocess.DEVNULL,
            )
            if p.returncode == 0 and p.stdout.strip():
                shell.socket.send(f"brilho atual: {p.stdout.strip()}\n".encode())
            else:
                shell.socket.send(b"erro: nao foi possivel ler o brilho\n")
            return
        valor = int(arg)
    except ValueError:
        shell.socket.send(b"uso: /bright [0-255]\n")
        return
    if valor < 0 or valor > 255:
        shell.socket.send(b"erro: brilho deve ser 0-255\n")
        return
    try:
        p = subprocess.run(
            ["termux-brightness", str(valor)],
            capture_output=True, text=True, timeout=10,
            stdin=subprocess.DEVNULL,
        )
        if p.returncode == 0:
            shell.socket.send(f"brilho = {valor}\n".encode())
        else:
            shell.socket.send(f"erro: {p.stderr or p.stdout or p.returncode}\n".encode())
    except FileNotFoundError:
        shell.socket.send(b"erro: termux-brightness nao instalado\n")
    except subprocess.TimeoutExpired:
        shell.socket.send(b"erro: timeout\n")
    except Exception as e:
        shell.socket.send(f"erro: {e}\n".encode())
