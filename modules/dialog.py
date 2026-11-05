import json
import subprocess

NAME = "/dialog"
DESC = "caixa de dialogo: /dialog <text|confirm|radio|spinner|date|time> [args]"


def _run(args_list, timeout=30):
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
    partes = args.strip().split(None, 1)
    if not partes:
        shell.socket.send(b"uso: /dialog text|confirm|radio|spinner|date|time\n")
        return

    tipo = partes[0].lower()
    resto = partes[1] if len(partes) > 1 else ""

    if tipo == "text":
        _text(shell, resto)
    elif tipo == "confirm":
        _confirm(shell, resto)
    elif tipo == "radio":
        _radio(shell, resto)
    elif tipo == "spinner":
        _spinner(shell, resto)
    elif tipo == "date":
        _date(shell)
    elif tipo == "time":
        _time(shell)
    else:
        shell.socket.send(f"tipo desconhecido: {tipo}\n".encode())


def _parse_json(raw):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _text(shell, dica):
    dica = dica.strip() or "Digite:"
    rc, out, err = _run(["termux-dialog", "text", "-t", dica])
    if rc != 0:
        shell.socket.send(f"erro: {err or rc}\n".encode())
        return
    d = _parse_json(out)
    if d and d.get("code") == -2:
        shell.socket.send(b"cancelado\n")
        return
    if d and "text" in d:
        shell.socket.send(f"resultado: {d['text']}\n".encode())
    else:
        shell.socket.send((out + "\n").encode())


def _confirm(shell, pergunta):
    pergunta = pergunta.strip() or "Confirmar?"
    rc, out, err = _run(["termux-dialog", "confirm", "-t", pergunta])
    if rc != 0:
        shell.socket.send(f"erro: {err or rc}\n".encode())
        return
    d = _parse_json(out)
    if d and "text" in d:
        shell.socket.send(f"resposta: {d['text']}\n".encode())
    else:
        shell.socket.send((out + "\n").encode())


def _radio(shell, opcoes):
    opcoes = opcoes.strip()
    if not opcoes:
        shell.socket.send(b"uso: /dialog radio op1,op2,op3\n")
        return
    rc, out, err = _run(["termux-dialog", "radio", "-v", opcoes])
    if rc != 0:
        shell.socket.send(f"erro: {err or rc}\n".encode())
        return
    d = _parse_json(out)
    if d and "text" in d:
        shell.socket.send(f"escolha: {d['text']}\n".encode())
    else:
        shell.socket.send((out + "\n").encode())


def _spinner(shell, opcoes):
    opcoes = opcoes.strip()
    if not opcoes:
        shell.socket.send(b"uso: /dialog spinner op1,op2,op3\n")
        return
    rc, out, err = _run(["termux-dialog", "spinner", "-v", opcoes])
    if rc != 0:
        shell.socket.send(f"erro: {err or rc}\n".encode())
        return
    d = _parse_json(out)
    if d and "text" in d:
        shell.socket.send(f"escolha: {d['text']}\n".encode())
    else:
        shell.socket.send((out + "\n").encode())


def _date(shell):
    rc, out, err = _run(["termux-dialog", "date"])
    if rc != 0:
        shell.socket.send(f"erro: {err or rc}\n".encode())
        return
    d = _parse_json(out)
    if d and "text" in d:
        shell.socket.send(f"data: {d['text']}\n".encode())
    else:
        shell.socket.send((out + "\n").encode())


def _time(shell):
    rc, out, err = _run(["termux-dialog", "time"])
    if rc != 0:
        shell.socket.send(f"erro: {err or rc}\n".encode())
        return
    d = _parse_json(out)
    if d and "text" in d:
        shell.socket.send(f"hora: {d['text']}\n".encode())
    else:
        shell.socket.send((out + "\n").encode())
