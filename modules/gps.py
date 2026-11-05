import json
import subprocess

NAME = "/gps"
DESC = "localizacao: /gps [gps|network|passive] (padrao: gps)"


def run(shell, args):
    
    provider = args.strip().lower() or "gps"
    if provider not in ("gps", "network", "passive"):
        shell.socket.send(b"uso: /gps [gps|network|passive]\n")
        return

    try:
        cmd = subprocess.run(
            ["termux-location", "-p", provider],
            capture_output=True,
            text=True,
            timeout=60,  
            stdin=subprocess.DEVNULL,
        )
        
        if cmd.returncode != 0:
            out = f"erro: {cmd.stderr or cmd.stdout or cmd.returncode}\n"
        else:
            out = _format(cmd.stdout, provider)
            
    except FileNotFoundError:
        out = "erro: termux-location nao instalado (pkg install termux-api)\n"
    except subprocess.TimeoutExpired:
        out = "erro: timeout (GPS pode demorar; tente 'network' ou va para area aberta)\n"
    except Exception as e:
        out = f"erro: {e}\n"

    shell.socket.send(out.encode())


def _format(raw, provider):
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        return raw if raw.endswith("\n") else raw + "\n"

    linhas = [
        f"provider : {d.get('provider', provider)}",
        f"latitude : {d.get('latitude', '?')}",
        f"longitude: {d.get('longitude', '?')}",
        f"altitude : {d.get('altitude', '?')} m",
        f"precisao : {d.get('accuracy', '?')} m",
        f"velocid. : {d.get('speed', '?')} m/s",
    ]
    return "\n".join(linhas) + "\n"
