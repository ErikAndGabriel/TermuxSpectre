import json
import subprocess

NAME = "/battery"
DESC = "status da bateria (formatado)"


def run(shell, args):
    try:
        cmd = subprocess.run(
            ["termux-battery-status"],
            capture_output=True,
            text=True,
            timeout=10,
            stdin=subprocess.DEVNULL,
        )
        if cmd.returncode != 0:
            out = f"erro: {cmd.stderr or cmd.stdout or cmd.returncode}\n"
        else:
            out = _format(cmd.stdout)
    except FileNotFoundError:
        out = "erro: termux-battery-status nao instalado (pkg install termux-api)\n"
    except subprocess.TimeoutExpired:
        out = "erro: timeout - verifique o app Termux:API\n"
    except Exception as e:
        out = f"erro: {e}\n"

    shell.socket.send(out.encode())


def _format(raw):
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        return raw if raw.endswith("\n") else raw + "\n"

    pct = d.get("percentage", "?")
    status = d.get("status", "?")
    plugged = d.get("plugged", "?")
    health = d.get("health", "?")
    temp = d.get("temperature", "?")
    volt = d.get("voltage", "?")
    cur = d.get("current", "?")

    if isinstance(cur, (int, float)):
        cur_txt = f"{cur / 1000:.0f} mA"
    else:
        cur_txt = str(cur)

    linhas = [
        f"bateria : {pct}%",
        f"status  : {status}",
        f"plug    : {plugged}",
        f"saude   : {health}",
        f"temp    : {temp} C",
        f"voltagem: {volt} mV",
        f"corrente: {cur_txt}",
    ]
    return "\n".join(linhas) + "\n"
