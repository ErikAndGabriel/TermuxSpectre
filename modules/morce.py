import subprocess
import time

NAME = "/morse"
DESC = "pisca lanterna em morse: /morse <texto>"


MORSE = {
    "a": ".-",    "b": "-...",  "c": "-.-.",  "d": "-..",
    "e": ".",     "f": "..-.",  "g": "--.",   "h": "....",
    "i": "..",    "j": ".---",  "k": "-.-",   "l": ".-..",
    "m": "--",    "n": "-.",    "o": "---",   "p": ".--.",
    "q": "--.-",  "r": ".-.",   "s": "...",   "t": "-",
    "u": "..-",   "v": "...-",  "w": ".--",   "x": "-..-",
    "y": "-.--",  "z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.",
}


def _torch(estado):
    try:
        subprocess.run(
            ["termux-torch", estado],
            capture_output=True, timeout=5,
            stdin=subprocess.DEVNULL,
        )
    except Exception:
        pass


def run(shell, args):
    texto = args.strip().lower()
    if not texto:
        shell.socket.send(b"uso: /morse <texto>\n")
        return

    codigo = []
    for c in texto:
        if c == " ":
            codigo.append("/")
        elif c in MORSE:
            codigo.append(MORSE[c])

    shell.socket.send((" ".join(codigo) + "\n").encode())

    try:
        for c in texto:
            if c == " ":
                time.sleep(0.9)
            elif c in MORSE:
                for s in MORSE[c]:
                    _torch("on")
                    time.sleep(0.15 if s == "." else 0.45)
                    _torch("off")
                    time.sleep(0.15)
                time.sleep(0.45)
    except Exception as e:
        shell.socket.send(f"erro: {e}\n".encode())
    finally:
        _torch("off")
