PORTAS = {
    20:    ("FTP-data",      "arquivo"),
    21:    ("FTP",           "arquivo"),
    22:    ("SSH",           "remoto"),
    23:    ("Telnet",        "remoto"),
    25:    ("SMTP",          "email"),
    53:    ("DNS",           "rede"),
    67:    ("DHCP-serv",     "rede"),
    68:    ("DHCP-cli",      "rede"),
    69:    ("TFTP",          "arquivo"),
    80:    ("HTTP",          "web"),
    110:   ("POP3",          "email"),
    111:   ("rpcbind",       "rede"),
    123:   ("NTP",           "rede"),
    135:   ("MSRPC",         "windows"),
    137:   ("NetBIOS-NS",    "windows"),
    138:   ("NetBIOS-DGM",   "windows"),
    139:   ("NetBIOS",       "windows"),
    143:   ("IMAP",          "email"),
    161:   ("SNMP",          "rede"),
    162:   ("SNMP-trap",     "rede"),
    179:   ("BGP",           "rede"),
    389:   ("LDAP",          "diretorio"),
    443:   ("HTTPS",         "web"),
    445:   ("SMB",           "windows"),
    465:   ("SMTPS",         "email"),
    500:   ("IKE/IPSec",     "rede"),
    514:   ("Syslog",        "rede"),
    515:   ("LPD",           "impressora"),
    548:   ("AFP",           "apple"),
    554:   ("RTSP",          "camera"),
    587:   ("SMTP-sub",      "email"),
    623:   ("IPMI",          "hardware"),
    631:   ("IPP",           "impressora"),
    636:   ("LDAPS",         "diretorio"),
    873:   ("rsync",         "arquivo"),
    902:   ("VMware",        "virtual"),
    989:   ("FTPS-data",     "arquivo"),
    990:   ("FTPS",          "arquivo"),
    993:   ("IMAPS",         "email"),
    995:   ("POP3S",         "email"),
    1080:  ("SOCKS",         "proxy"),
    1194:  ("OpenVPN",       "vpn"),
    1433:  ("MSSQL",         "banco"),
    1521:  ("Oracle",        "banco"),
    1701:  ("L2TP",          "vpn"),
    1720:  ("H.323",         "voip"),
    1723:  ("PPTP",          "vpn"),
    1883:  ("MQTT",          "iot"),
    1900:  ("UPnP",          "rede"),
    2000:  ("Cisco-SCCP",    "voip"),
    2049:  ("NFS",           "arquivo"),
    2181:  ("Zookeeper",     "cluster"),
    2222:  ("SSH-alt",       "remoto"),
    2375:  ("Docker-API",    "container"),
    2376:  ("Docker-TLS",    "container"),
    3000:  ("Grafana/Node",  "web"),
    3128:  ("Squid",         "proxy"),
    3260:  ("iSCSI",         "storage"),
    3306:  ("MySQL",         "banco"),
    3389:  ("RDP",           "windows"),
    3478:  ("STUN/TURN",     "voip"),
    4369:  ("Erlang-EPMD",   "cluster"),
    4444:  ("suspeito",      "suspeito"),
    4445:  ("backdoor",      "suspeito"),
    4500:  ("NAT-T/IPSec",   "rede"),
    5000:  ("UPnP/Flask",    "web"),
    5060:  ("SIP",           "voip"),
    5061:  ("SIP-TLS",       "voip"),
    5222:  ("XMPP",          "mensagem"),
    5353:  ("mDNS",          "rede"),
    5432:  ("PostgreSQL",    "banco"),
    5555:  ("ADB",           "android"),
    5601:  ("Kibana",        "web"),
    5672:  ("AMQP",          "mensageria"),
    5900:  ("VNC",           "remoto"),
    5984:  ("CouchDB",       "banco"),
    5985:  ("WinRM",         "windows"),
    5986:  ("WinRM-TLS",     "windows"),
    6379:  ("Redis",         "banco"),
    6443:  ("K8s-API",       "container"),
    6667:  ("IRC",           "suspeito"),
    7000:  ("AirPlay",       "apple"),
    7443:  ("HTTPS-alt",     "web"),
    7547:  ("TR-069",        "roteador"),
    8000:  ("HTTP-alt",      "web"),
    8080:  ("HTTP-alt",      "web"),
    8081:  ("HTTP-alt",      "web"),
    8086:  ("InfluxDB",      "banco"),
    8123:  ("HomeAssistant", "iot"),
    8443:  ("HTTPS-alt",     "web"),
    8500:  ("Consul",        "cluster"),
    8883:  ("MQTT/TLS",      "iot"),
    8888:  ("HTTP-alt",      "web"),
    9000:  ("Portainer",     "container"),
    9090:  ("Prometheus",    "web"),
    9100:  ("JetDirect",     "impressora"),
    9200:  ("Elasticsearch", "banco"),
    9418:  ("Git",           "dev"),
    9443:  ("HTTPS-alt",     "web"),
    10000: ("Webmin",        "admin"),
    11211: ("Memcached",     "cache"),
    13306: ("MySQL-alt",     "banco"),
    1337:  ("backdoor",      "suspeito"),
    19132: ("Minecraft-BE",  "jogo"),
    25565: ("Minecraft-JE",  "jogo"),
    27015: ("Source-Engine", "jogo"),
    27017: ("MongoDB",       "banco"),
    31337: ("backdoor",      "suspeito"),
    32400: ("Plex",          "midia"),
    49152: ("UPnP-dyn",      "rede"),
    51820: ("WireGuard",     "vpn"),
    62078: ("lockdownd",     "apple"),
}


COMBINACOES = [
    ({62078},              "iPhone/iPad",                "certeza", "lockdownd e exclusivo de iOS"),
    ({7000, 62078},        "iPhone/iPad (AirPlay)",      "certeza", "lockdownd + AirPlay"),
    ({548, 62078},         "Mac (AFP + iOS)",            "alta",    "AFP + lockdownd"),

    ({5555, 8080},         "Android com servidor web",   "alta",    "ADB + HTTP = celular exposto"),
    ({5555},               "Android (ADB)",              "alta",    "ADB ativo (depuracao USB sem fio)"),

    ({7547},               "roteador (TR-069)",          "certeza", "TR-069 e protocolo de ISP"),
    ({53, 80, 443, 1900},  "roteador",                   "certeza", "stack completa de gateway"),
    ({53, 80, 443},        "roteador",                   "alta",    "DNS + HTTP + HTTPS = gateway"),
    ({53, 1900},           "roteador",                   "alta",    "DNS + UPnP = gateway"),
    ({53, 67},             "roteador (DHCP)",            "alta",    "DNS + DHCP = gateway"),

    ({554, 80},            "camera IP",                  "alta",    "RTSP + HTTP = camera web"),
    ({554, 443},           "camera IP (web segura)",     "alta",    "RTSP + HTTPS"),
    ({554},                "camera IP",                  "alta",    "RTSP e streaming de camera"),
    ({32400, 1900},        "servidor Plex (DLNA)",       "alta",    "Plex + UPnP"),
    ({32400},              "servidor Plex",              "alta",    "Plex Media Server"),

    ({631, 9100},          "impressora (multifuncional)","certeza", "IPP + JetDirect"),
    ({631},                "impressora",                 "certeza", "IPP e protocolo de impressora"),
    ({9100},               "impressora",                 "alta",    "JetDirect e porta de impressora"),
    ({515},                "impressora (LPD)",           "alta",    "LPD classico"),

    ({1883, 8883},         "broker MQTT",                "alta",    "MQTT + MQTT/TLS"),
    ({1883},               "IoT (MQTT)",                 "alta",    "MQTT e protocolo de IoT"),
    ({8883},               "IoT (MQTT/TLS)",             "alta",    "MQTT sobre TLS"),
    ({8123},               "Home Assistant",             "alta",    "porta padrao do HA"),

    ({135, 139, 445},      "Windows (dominio)",          "certeza", "MSRPC + SMB"),
    ({139, 445},           "Windows",                    "certeza", "SMB = compartilhamento Windows"),
    ({5985},               "Windows (WinRM)",            "alta",    "WinRM HTTP"),
    ({5986},               "Windows (WinRM-TLS)",        "alta",    "WinRM HTTPS"),
    ({3389},               "Windows (RDP)",              "alta",    "RDP e area de trabalho remota"),

    ({22, 80, 443},        "servidor web (Linux)",       "alta",    "SSH + web completa"),
    ({22, 3306},           "servidor (SSH + MySQL)",     "alta",    "Linux com banco"),
    ({22, 5432},           "servidor (SSH + Postgres)",  "alta",    "Linux com banco"),
    ({22, 6379},           "servidor (SSH + Redis)",     "alta",    "Linux com cache"),
    ({22, 80},             "servidor (SSH + web)",       "alta",    "Linux exposto"),
    ({22},                 "servidor/NAS",               "baixa",   "SSH sozinho e ambiguo"),

    ({27017},              "servidor MongoDB",           "alta",    "MongoDB exposto"),
    ({9200},               "Elasticsearch",              "alta",    "ES exposto (risco)"),
    ({11211},              "Memcached",                  "alta",    "cache exposto (risco)"),
    ({3306},               "servidor MySQL",             "media",   "porta padrao MySQL"),
    ({5432},               "servidor PostgreSQL",        "media",   "porta padrao Postgres"),
    ({1433},               "servidor MSSQL",             "media",   "porta padrao SQL Server"),

    ({2375},               "Docker exposto",             "alta",    "Docker API sem TLS (risco critico)"),
    ({2376},               "Docker (TLS)",               "alta",    "Docker API com TLS"),
    ({6443},               "Kubernetes API",             "alta",    "kube-apiserver"),
    ({2375, 6443},         "cluster K8s/Docker",         "alta",    "orquestracao exposta"),
    ({9000},               "Portainer/Container UI",     "media",   "porta padrao do Portainer"),
    ({8080, 9000},         "possivel Portainer",         "baixa",   "9000 + 8080 e ambiguo"),

    ({5060, 5061},         "PBX/VoIP (SIP/TLS)",         "alta",    "SIP + SIP-TLS"),
    ({5060},               "PBX/VoIP (SIP)",             "alta",    "SIP padrao"),

    ({1194},               "servidor OpenVPN",           "alta",    "OpenVPN padrao"),
    ({51820},              "servidor WireGuard",         "alta",    "WireGuard padrao"),
    ({1080},               "proxy SOCKS",                "media",   "SOCKS exposto"),
    ({3128},               "proxy Squid",                "media",   "proxy HTTP"),

    ({9418},               "servidor Git",               "alta",    "git protocol"),
    ({10000},              "Webmin",                     "alta",    "painel admin"),

    ({25565},              "servidor Minecraft",         "alta",    "Minecraft Java Edition"),
    ({19132},              "servidor Minecraft BE",      "alta",    "Minecraft Bedrock"),
    ({27015},              "servidor Source",            "alta",    "Source Engine (CS, TF2...)"),

    ({80},                 "dispositivo com web",        "baixa",   "HTTP sozinho e ambiguo"),
    ({443},                "dispositivo com web",        "baixa",   "HTTPS sozinho e ambiguo"),
    ({8080},               "dispositivo com web",        "baixa",   "HTTP alternativo"),
    ({8443},               "dispositivo com web",        "baixa",   "HTTPS alternativo"),

    ({4444, 6667},         "SUSPEITO (C2)",              "alta",    "payload + IRC = botnet"),
    ({31337},              "SUSPEITO (backdoor)",        "alta",    "porta classica de backdoor"),
    ({1337},               "SUSPEITO (backdoor)",        "alta",    "porta classica de backdoor"),
    ({6667},               "SUSPEITO (botnet IRC)",      "media",   "IRC frequentemente usado por botnet"),
    ({4444},               "porta suspeita",             "media",   "4444 e comum em payloads e apps legitimos"),
]


def descrever(porta):
    return PORTAS.get(porta, ("desconhecido", "?"))


def inferir(portas_abertas):
    abertas = set(portas_abertas)
    for combinacao, nome, confianca, motivo in COMBINACOES:
        if combinacao.issubset(abertas):
            return {
                "dispositivo": nome,
                "confianca": confianca,
                "motivo": motivo,
            }
    return {
        "dispositivo": "desconhecido",
        "confianca": "baixa",
        "motivo": "nenhuma combinacao conhecida",
    }


def servicos(portas_abertas):
    return [f"{p}/{descrever(p)[0]}" for p in portas_abertas]


def classificar(portas_abertas):
    grupos = {}
    for p in portas_abertas:
        _, categoria = descrever(p)
        grupos.setdefault(categoria, []).append(p)
    return grupos
