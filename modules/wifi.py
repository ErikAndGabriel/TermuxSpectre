import json
import subprocess

NAME = "/wifi"
DESC = "wifi: /wifi (conexao atual) | /wifi scan (redes proximas)"


def run(shell, args):
    sub = args.strip().lower()

    if sub == "scan":
        _scan(shell)
    else:
        _conexao(shell)


def _conexao(shell):
    try:
        cmd = subprocess.run(
            ["termux-wifi-connectioninfo"],
            capture_output=True,
            text=True,
            timeout=10,
            stdin=subprocess.DEVNULL,
        )
        if cmd.returncode != 0:
            out = f"erro: {cmd.stderr or cmd.stdout or cmd.returncode}\n"
        else:
            data = json.loads(cmd.stdout)
            out = (
                f"SSID    : {data.get('ssid', '?')}\n"
                f"BSSID   : {data.get('bssid', '?')}\n"
                f"IP      : {data.get('ip', '?')}\n"
                f"Sinal   : {data.get('rssi', '?')} dBm\n"
                f"Veloc.  : {data.get('link_speed_mbps', '?')} Mbps\n"
                f"Freq.   : {data.get('frequency_mhz', '?')} MHz\n"
            )
    except FileNotFoundError:
        out = "erro: termux-wifi-connectioninfo nao instalado\n"
    except subprocess.TimeoutExpired:
        out = "erro: timeout (verifique permissao de localizacao)\n"
    except json.JSONDecodeError:
        out = f"erro: saida invalida da API\n{cmd.stdout[:200]}\n"
    except Exception as e:
        out = f"erro: {e}\n"

    shell.socket.send(out.encode())


def _scan(shell):
    try:
        cmd = subprocess.run(
            ["termux-wifi-scaninfo"],
            capture_output=True,
            text=True,
            timeout=20,
            stdin=subprocess.DEVNULL,
        )
        if cmd.returncode != 0:
            out = f"erro: {cmd.stderr or cmd.stdout or cmd.returncode}\n"
        else:
            redes = json.loads(cmd.stdout)
            if not redes:
                out = "nenhuma rede encontrada\n"
            else:
                redes.sort(key=lambda r: r.get("rssi", -999), reverse=True)
                linhas = [f"total: {len(redes)}\n"]
                for r in redes:
                    ssid = r.get("ssid") or "(oculta)"
                    bssid = r.get("bssid", "?")
                    rssi = r.get("rssi", "?")
                    freq = r.get("frequency", "?")
                    linhas.append(
                        f"{ssid:<20} {bssid:<18} {rssi:>4} dBm  {freq} MHz"
                    )
                out = "\n".join(linhas) + "\n"
    except FileNotFoundError:
        out = "erro: termux-wifi-scaninfo nao instalado\n"
    except subprocess.TimeoutExpired:
        out = "erro: timeout no scan (20s)\n"
    except json.JSONDecodeError:
        out = f"erro: saida invalida da API\n{cmd.stdout[:200]}\n"
    except Exception as e:
        out = f"erro: {e}\n"

    shell.socket.send(out.encode())
