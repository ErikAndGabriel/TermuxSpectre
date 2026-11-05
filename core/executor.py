import os
import subprocess

class CommandExecutor:
    def run(self, command: str) -> bytes:
        if command.startswith("cd "):
            try:
                os.chdir(command[3:].strip())
                return b""
            except OSError as e:
                return f"[-] cd error: {e}\n".encode()

        try:
            p = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                timeout=30,
            )
            return p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            return b"[-] timeout\n"
        except Exception as e:
            return f"[-] error: {e}\n".encode()
