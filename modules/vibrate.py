import subprocess

NAME = "/vibrate"
DESC = "vibra o aparelho: /vibrate [ms] (padrao 500)"


def run(shell, args):
    try:
        ms = int(args.strip()) if args.strip() else 500
    except ValueError:
        shell.socket.send(b"uso: /vibrate [ms] (1-5000)\n")
        return
    if ms < 1 or ms > 5000:
        shell.socket.send(b"erro: ms deve ser 1-5000\n")
        return
    try:
        p = subprocess.run(
            ["termux-vibrate", "-d", str(ms), "-f"],
            capture_output=True, text=True, timeout=10,
            stdin=subprocess.DEVNULL,
        )
        if p.returncode == 0:
            shell.socket.send(f"vibrando {ms}ms\n".encode())
        else:
            shell.socket.send(f"erro: {p.stderr or p.stdout or p.returncode}\n".encode())
    except FileNotFoundError:
        shell.socket.send(b"erro: termux-vibrate nao instalado\n")
    except subprocess.TimeoutExpired:
        shell.socket.send(b"erro: timeout\n")
    except Exception as e:
        shell.socket.send(f"erro: {e}\n".encode())
