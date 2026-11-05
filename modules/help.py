NAME = "/help"
DESC = "lista os comandos disponiveis"


def run(shell, args):
    amarelo = "\033[33m"
    ciano = "\033[36m"
    verde = "\033[32m"
    cinza = "\033[90m"
    reset = "\033[0m"

    linhas = [f"{ciano}comandos:{reset}"]

    for nome, mod in sorted(shell.commands.items()):
        desc = getattr(mod, "DESC", "")
        linhas.append(f"  {amarelo}{nome:<14}{reset} {verde}{desc}{reset}")

    linhas.append("")
    linhas.append(f"{cinza}total: {len(shell.commands)} comandos{reset}")

    shell.socket.send(("\n".join(linhas) + "\n").encode())
