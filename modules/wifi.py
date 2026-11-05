import json
import subprocess

NAME = "/wifi"
DESC = "informacoes da conexao Wi-Fi (SSID, IP, sinal)"


def run(shell, args):
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
        out = "erro: termux-wifi-connectioninfo nao instalado (pkg install termux-api)\n"
    except subprocess.TimeoutExpired:
        out = "erro: timeout (verifique se o app Termux:API tem permissao de localizacao)\n"
    except json.JSONDecodeError:
        out = f"erro: saida invalida da API\n{cmd.stdout[:200]}\n"
    except Exception as e:
        out = f"erro: {e}\n"

    shell.socket.send(out.encode())
