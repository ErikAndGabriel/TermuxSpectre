import subprocess

NAME = "/notification"
DESC = "envia notificacao: /notification <titulo> | <texto>"


def run(shell, args):
    if "|" not in args:
        shell.socket.send(b"uso: /notification <titulo> | <texto>\n")
        return

    title, _, text = args.partition("|")
    title = title.strip()
    text = text.strip()

    if not title or not text:
        shell.socket.send(b"uso: /notification <titulo> | <texto>\n")
        return

    try:
        cmd = subprocess.run(
            [
                "termux-notification",
                "--title", title,
                "--content", text,
            ],
            capture_output=True,
            text=True,
            timeout=10,
            stdin=subprocess.DEVNULL,
        )
        if cmd.returncode == 0:
            out = f"ok: notificacao enviada\n"
        else:
            out = f"erro: {cmd.stderr or cmd.stdout or cmd.returncode}\n"
    except FileNotFoundError:
        out = "erro: termux-notification nao instalado (pkg install termux-api)\n"
    except subprocess.TimeoutExpired:
        out = "erro: timeout\n"
    except Exception as e:
        out = f"erro: {e}\n"

    shell.socket.send(out.encode())
