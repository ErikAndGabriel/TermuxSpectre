import os

NAME = "/persist"
DESC = "persistencia: /persist install|remove|status"

BOOT_DIR = os.path.expanduser("~/.termux/boot")
BOOT_SCRIPT = os.path.join(BOOT_DIR, "start-spectre.sh")
BASHRC = os.path.expanduser("~/.bashrc")
MARKER = "# TermuxSpectre persist"


SCRIPT = """#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
cd ~/TermuxSpectre
for i in 1 2 3; do
    if timeout 3 bash -c "echo > /dev/tcp/127.0.0.1/4444" 2>/dev/null; then
        nohup python main.py > /dev/null 2>&1 &
        break
    fi
    sleep 5
done
"""


def run(shell, args):
    sub = args.strip().lower() or "status"

    if sub == "install":
        _install(shell)
    elif sub == "remove":
        _remove(shell)
    elif sub == "status":
        _status(shell)
    else:
        shell.socket.send(b"uso: /persist install|remove|status\n")


def _install(shell):
    linhas = []

    try:
        os.makedirs(BOOT_DIR, exist_ok=True)
        with open(BOOT_SCRIPT, "w") as f:
            f.write(SCRIPT)
        os.chmod(BOOT_SCRIPT, 0o755)
        linhas.append(f"boot script: {BOOT_SCRIPT}")
    except Exception as e:
        linhas.append(f"erro boot: {e}")

    try:
        with open(BASHRC, "r") as f:
            conteudo = f.read()
    except FileNotFoundError:
        conteudo = ""

    if MARKER not in conteudo:
        bloco = (
            f"\n{MARKER}\n"
            f"if ! pgrep -f 'python main.py' > /dev/null; then\n"
            f"    cd ~/TermuxSpectre && nohup python main.py > /dev/null 2>&1 &\n"
            f"fi\n"
        )
        try:
            with open(BASHRC, "a") as f:
                f.write(bloco)
            linhas.append(f"bashrc: bloco adicionado")
        except Exception as e:
            linhas.append(f"erro bashrc: {e}")
    else:
        linhas.append("bashrc: ja instalado")

    linhas.append("aviso: instale o app Termux:Boot e abra uma vez")
    shell.socket.send(("\n".join(linhas) + "\n").encode())


def _remove(shell):
    linhas = []

    if os.path.exists(BOOT_SCRIPT):
        try:
            os.remove(BOOT_SCRIPT)
            linhas.append("boot script removido")
        except Exception as e:
            linhas.append(f"erro boot: {e}")
    else:
        linhas.append("boot script: nao existia")

    try:
        with open(BASHRC, "r") as f:
            linhas_arq = f.readlines()
    except FileNotFoundError:
        linhas_arq = []

    if any(MARKER in l for l in linhas_arq):
        novo = []
        pular = 0
        for l in linhas_arq:
            if MARKER in l:
                pular = 3
                continue
            if pular > 0:
                pular -= 1
                continue
            novo.append(l)
        with open(BASHRC, "w") as f:
            f.writelines(novo)
        linhas.append("bashrc: bloco removido")
    else:
        linhas.append("bashrc: nao estava instalado")

    shell.socket.send(("\n".join(linhas) + "\n").encode())


def _status(shell):
    linhas = []

    linhas.append(f"boot script: {'sim' if os.path.exists(BOOT_SCRIPT) else 'nao'}")

    try:
        with open(BASHRC, "r") as f:
            tem = MARKER in f.read()
    except FileNotFoundError:
        tem = False
    linhas.append(f"bashrc    : {'sim' if tem else 'nao'}")

    try:
        import subprocess
        p = subprocess.run(
            ["pgrep", "-f", "python main.py"],
            capture_output=True, text=True,
            timeout=5, stdin=subprocess.DEVNULL,
        )
        rodando = p.returncode == 0
    except Exception:
        rodando = False
    linhas.append(f"processo  : {'rodando' if rodando else 'parado'}")

    shell.socket.send(("\n".join(linhas) + "\n").encode())
