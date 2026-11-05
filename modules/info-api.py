import json
import subprocess

NAME = "/info-api"
DESC = "info do aparelho: /info-api sensor|device|cell [args]"


def _run(args_list, timeout=15):
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


def _parse(raw):
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


def run(shell, args):
    partes = args.strip().split(None, 1)
    if not partes:
        shell.socket.send(b"uso: /info-api sensor|device|cell [args]\n")
        return

    sub = partes[0].lower()
    resto = partes[1] if len(partes) > 1 else ""

    if sub == "sensor":
        _sensor(shell, resto)
    elif sub == "device":
        _device(shell)
    elif sub == "cell":
        _cell(shell)
    else:
        shell.socket.send(f"subcomando desconhecido: {sub}\n".encode())


def _sensor(shell, args):
    alvo = args.strip()
    if not alvo or alvo.lower() == "list":
        rc, out, err = _run(["termux-sensor", "-l"])
        if rc == 0:
            shell.socket.send((out + "\n").encode())
        else:
            shell.socket.send(f"erro: {err or out or rc}\n".encode())
        return

    rc, out, err = _run(
        ["termux-sensor", "-s", alvo, "-n", "1"],
        timeout=20,
    )
    if rc != 0:
        shell.socket.send(f"erro: {err or out or rc}\n".encode())
        return

    data = _parse(out)
    if not data or not isinstance(data, dict):
        shell.socket.send((out + "\n").encode())
        return

    linhas = [f"sensor: {alvo}"]
    for nome, valores in data.items():
        if isinstance(valores, dict):
            for k, v in valores.items():
                linhas.append(f"  {k:<14} {v}")
        elif isinstance(valores, list):
            for i, v in enumerate(valores, 1):
                linhas.append(f"  [{i}] {v}")
        else:
            linhas.append(f"  {nome:<14} {valores}")
    shell.socket.send(("\n".join(linhas) + "\n").encode())


def _device(shell):
    rc, out, err = _run(["termux-telephony-deviceinfo"])
    if rc != 0:
        shell.socket.send(f"erro: {err or out or rc}\n".encode())
        return

    data = _parse(out)
    if not data or not isinstance(data, dict):
        shell.socket.send((out + "\n").encode())
        return

    campos = [
        ("network_operator_name", "operadora"),
        ("network_country_iso", "pais"),
        ("network_type", "rede"),
        ("sim_state", "sim"),
        ("sim_operator_name", "operadora_sim"),
        ("sim_country_iso", "pais_sim"),
        ("device_id", "imei"),
        ("software_version", "versao_sw"),
        ("data_state", "dados"),
        ("call_state", "chamada"),
    ]

    linhas = ["[ dispositivo de telefonia ]"]
    for chave, label in campos:
        valor = data.get(chave)
        if valor is not None:
            linhas.append(f"  {label:<14} {valor}")

    if len(linhas) == 1:
        linhas.append((out + "\n"))
        shell.socket.send(("".join(linhas)).encode())
        return

    shell.socket.send(("\n".join(linhas) + "\n").encode())


def _cell(shell):
    rc, out, err = _run(["termux-telephony-cellinfo"])
    if rc != 0:
        shell.socket.send(f"erro: {err or out or rc}\n".encode())
        return

    data = _parse(out)
    if not data or not isinstance(data, list):
        shell.socket.send((out + "\n").encode())
        return

    if not data:
        shell.socket.send(b"nenhuma torre visivel (modo aviao ou wifi only)\n")
        return

    linhas = [f"[ torres: {len(data)} ]"]
    for i, torre in enumerate(data, 1):
        tipo = torre.get("type", "?")
        registrada = "registrada" if torre.get("registered") else "vizinh"
        linhas.append(f"  [{i}] {tipo.upper()} ({registrada})")

        if "cid" in torre:
            linhas.append(f"      cid     : {torre['cid']}")
        if "lac" in torre:
            linhas.append(f"      lac     : {torre['lac']}")
        if "mcc" in torre:
            linhas.append(f"      mcc/mnc : {torre.get('mcc','?')}/{torre.get('mnc','?')}")
        if "signal_strength" in torre:
            linhas.append(f"      sinal   : {torre['signal_strength']} dBm")
        if "timing_advance" in torre:
            linhas.append(f"      timing  : {torre['timing_advance']}")

    shell.socket.send(("\n".join(linhas) + "\n").encode())
