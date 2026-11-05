import subprocess

NAME = "/clip"
DESC = "clipboard: /clip (le) | /clip <texto> (escreve)"


def run(shell, args):
    texto = args.strip()
    try:
        if not texto:
            p = subprocess.run(
                ["termux-clipboard-get"],
                capture_output=True, text=True, timeout=10,
                stdin=subprocess.DEVNULL,
            )
            if p.returncode == 0:
                shell.socket.send(f"clipboard: {p.stdout.strip() or '(vazio)'}\n".encode())
            else:
                shell.socket.send(f"erro: {p.stderr or p.returncode}\n".encode())
            return
        p = subprocess.run(
            ["termux-clipboard-set", texto],
            capture_output=True, text=True, timeout=10,
            stdin=subprocess.DEVNULL,
        )
        if p.returncode == 0:
            shell.socket.send(b"clipboard atualizado\n")
        else:
            shell.socket.send(f"erro: {p.stderr or p.stdout or p.returncode}\n".encode())
    except FileNotFoundError:
        shell.socket.send(b"erro: termux-clipboard nao instalado\n")
    except subprocess.TimeoutExpired:
        shell.socket.send(b"erro: timeout\n")
    except Exception as e:
        shell.socket.send(f"erro: {e}\n".encode())
