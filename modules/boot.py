import os
import subprocess

NAME = "/boot"
DESC = "status do termux-boot e scripts de inicializacao"

BOOT_DIR = os.path.expanduser("~/.termux/boot")


def run(shell, args):
    linhas = []

    linhas.append(f"pasta boot: {BOOT_DIR}")
    if os.path.isdir(BOOT_DIR):
        try:
            arquivos = sorted(os.listdir(BOOT_DIR))
        except Exception as e:
            shell.socket.send(f"erro: {e}\n".encode())
            return
        if arquivos:
            linhas.append("scripts:")
            for a in arquivos:
                caminho = os.path.join(BOOT_DIR, a)
                exec_ok = os.access(caminho, os.X_OK)
                linhas.append(f"  {a} {'[exec]' if exec_ok else '[sem +x]'}")
        else:
            linhas.append("nenhum script")
    else:
        linhas.append("pasta nao existe (rode /persist install)")

    try:
        p = subprocess.run(
            ["pm", "list", "packages", "com.termux.boot"],
            capture_output=True, text=True,
            timeout=10, stdin=subprocess.DEVNULL,
        )
        instalado = "com.termux.boot" in p.stdout
    except Exception:
        instalado = False

    linhas.append(f"app Termux:Boot: {'instalado' if instalado else 'NAO instalado'}")

    shell.socket.send(("\n".join(linhas) + "\n").encode())
