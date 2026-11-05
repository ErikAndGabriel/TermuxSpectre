import subprocess
import threading
import time

NAME = "/troll"
DESC = "modo caos controlado: /troll [segundos] (padrao 10)"


def _run(args_list):
    try:
        subprocess.run(
            args_list, capture_output=True,
            timeout=5, stdin=subprocess.DEVNULL,
        )
    except Exception:
        pass


def run(shell, args):
    try:
        dur = int(args.strip()) if args.strip() else 10
    except ValueError:
        shell.socket.send(b"uso: /troll [segundos] (1-60)\n")
        return

    dur = max(1, min(dur, 60))

    def worker():
        fim = time.time() + dur
        while time.time() < fim:
            _run(["termux-torch", "on"])
            _run(["termux-vibrate", "-d", "300", "-f"])
            time.sleep(0.4)
            _run(["termux-torch", "off"])
            time.sleep(0.3)

    threading.Thread(target=worker, daemon=True).start()
    shell.socket.send(f"troll ativado por {dur}s\n".encode())
