import os
import platform
import shutil
import socket
import subprocess

NAME = "/info"
DESC = "informacoes do sistema"


def _run(cmd_list, timeout=10):
    try:
        p = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            timeout=timeout,
            stdin=subprocess.DEVNULL,
        )
        return (p.stdout or p.stderr or "").strip()
    except FileNotFoundError:
        return "?"
    except subprocess.TimeoutExpired:
        return "timeout"
    except Exception as e:
        return f"err: {e}"


def _collect():
    linhas = []

    linhas.append("[ dispositivo ]")
    linhas.append(f"hostname : {socket.gethostname()}")
    linhas.append(f"modelo   : {_run(['getprop', 'ro.product.model'])}")
    linhas.append(f"marca    : {_run(['getprop', 'ro.product.brand'])}")
    linhas.append(f"android  : {_run(['getprop', 'ro.build.version.release'])}")
    linhas.append(f"sdk      : {_run(['getprop', 'ro.build.version.sdk'])}")
    linhas.append(f"arch     : {platform.machine()}")
    linhas.append(f"kernel   : {platform.release()}")

    linhas.append("")
    linhas.append("[ usuario ]")
    linhas.append(f"user     : {_run(['whoami'])}")
    linhas.append(f"uid      : {os.getuid()}")
    linhas.append(f"home     : {os.path.expanduser('~')}")
    linhas.append(f"pwd      : {os.getcwd()}")
    linhas.append(f"prefix   : {os.environ.get('PREFIX', '?')}")

    linhas.append("")
    linhas.append("[ python ]")
    linhas.append(f"versao   : {platform.python_version()}")
    linhas.append(f"exe      : {shutil.which('python') or '?'}")

    linhas.append("")
    linhas.append("[ rede ]")
    try:
        ip_local = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip_local = "?"
    linhas.append(f"ip local : {ip_local}")
    linhas.append(f"ifaces   : {_run(['ip', '-4', 'addr', 'show'], timeout=5).replace(chr(10), ' | ')[:120]}")

    linhas.append("")
    linhas.append("[ armazenamento ]")
    linhas.append(_run(["df", "-h", os.path.expanduser("~")]))

    linhas.append("")
    linhas.append("[ bateria ]")
    linhas.append(f"cap      : {_run(['cat', '/sys/class/power_supply/battery/capacity'])}%")
    linhas.append(f"status   : {_run(['cat', '/sys/class/power_supply/battery/status'])}")

    linhas.append("")
    linhas.append("[ uptime ]")
    linhas.append(_run(["uptime"]))

    return "\n".join(linhas)


def run(shell, args):
    out = _collect()
    if not out.endswith("\n"):
        out += "\n"
    shell.socket.send(out.encode())
