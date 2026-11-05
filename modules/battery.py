import subprocess

NAME = "/battery"
DESC = "status da bateria"


def run(shell, args):
    try:
        cmd = subprocess.run(
            ["termux-battery-status"],
            capture_output=True, text=True, timeout=5,
        )
        out = cmd.stdout if cmd.returncode == 0 else cmd.stderr
    except FileNotFoundError:
        out = "Error: termux-battery-status nao instalado"
    except subprocess.TimeoutExpired:
        out = "Error: timeout"
    except Exception as e:
        out = f"Error: {e}"
    if not out.endswith("\n"):
        out += "\n"
    shell.socket.send(out.encode())
