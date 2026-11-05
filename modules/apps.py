import subprocess

NAME = "/apps"
DESC = "lista apps instalados: /apps [filtro]"


def run(shell, args):
    filtro = args.strip().lower()

    try:
        cmd = subprocess.run(
            ["pm", "list", "packages"],
            capture_output=True,
            text=True,
            timeout=15,
            stdin=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        shell.socket.send(b"erro: pm nao encontrado (nao e Android?)\n")
        return
    except subprocess.TimeoutExpired:
        shell.socket.send(b"erro: timeout\n")
        return
    except Exception as e:
        shell.socket.send(f"erro: {e}\n".encode())
        return

    if cmd.returncode != 0:
        shell.socket.send(f"erro: {cmd.stderr or cmd.returncode}\n".encode())
        return

    pacotes = []
    for linha in cmd.stdout.splitlines():
        linha = linha.strip()
        if linha.startswith("package:"):
            pacote = linha[len("package:"):]
            if not filtro or filtro in pacote.lower():
                pacotes.append(pacote)

    if not pacotes:
        shell.socket.send(f"nenhum app encontrado{' com filtro: ' + filtro if filtro else ''}\n".encode())
        return

    pacotes.sort()
    cabecalho = f"total: {len(pacotes)}\n"
    corpo = "\n".join(pacotes)
    out = cabecalho + corpo + "\n"

    if len(out) > 8000:
        out = out[:8000] + f"\n... (truncado, use /apps <filtro> pra refinar)\n"

    shell.socket.send(out.encode())
