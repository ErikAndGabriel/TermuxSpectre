import subprocess

NAME = "/speak"
DESC = "fala um texto: /speak <texto>"


def run(shell, args):
    texto = args.strip()
    if not texto:
        shell.socket.send(b"uso: /speak <texto>\n")
        return

    try:
        cmd = subprocess.run(
            ["termux-tts-speak", texto],
            capture_output=True,
            text=True,
            timeout=30,
            stdin=subprocess.DEVNULL,
        )
        if cmd.returncode == 0:
            out = "ok: falando\n"
        else:
            out = f"erro: {cmd.stderr or cmd.stdout or cmd.returncode}\n"
    except FileNotFoundError:
        out = "erro: termux-tts-speak nao instalado (pkg install termux-api)\n"
    except subprocess.TimeoutExpired:
        out = "erro: timeout\n"
    except Exception as e:
        out = f"erro: {e}\n"

    shell.socket.send(out.encode())
