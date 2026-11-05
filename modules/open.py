import subprocess

NAME = "/open"
DESC = "abre app, site ou arquivo: /open <url|app|arquivo>"


def _run(args_list, timeout=10):
    try:
        p = subprocess.run(
            args_list,
            capture_output=True,
            text=True,
            timeout=timeout,
            stdin=subprocess.DEVNULL,
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except FileNotFoundError:
        return -1, "", f"{args_list[0]} nao instalado"
    except subprocess.TimeoutExpired:
        return -2, "", "timeout"
    except Exception as e:
        return -3, "", str(e)


def run(shell, args):
    target = args.strip()
    if not target:
        shell.socket.send(b"uso: /open <url|app|arquivo>\n")
        return
    if target.startswith(("http://", "https://")):
        rc, out, err = _run(["termux-open-url", target])
        if rc == 0:
            shell.socket.send(f"aberto: {target}\n".encode())
        else:
            shell.socket.send(f"erro: {err or out or rc}\n".encode())
        return

    if "://" in target or target.startswith(("mailto:", "tel:", "sms:")):
        rc, out, err = _run(["termux-open-url", target])
        if rc == 0:
            shell.socket.send(f"aberto: {target}\n".encode())
        else:
            shell.socket.send(f"erro: {err or out or rc}\n".encode())
        return

    if "." in target and not "/" in target and not " " in target:
        rc, out, err = _run(["termux-open", f"intent://#Intent;package={target};end"])
        if rc == 0:
            shell.socket.send(f"app aberto: {target}\n".encode())
        else:
            shell.socket.send(f"erro: {err or out or rc}\n".encode())
        return
    rc, out, err = _run(["termux-open", target])
    if rc == 0:
        shell.socket.send(f"aberto: {target}\n".encode())
    else:
        shell.socket.send(f"erro: {err or out or rc}\n".encode())
