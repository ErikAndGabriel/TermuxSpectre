import subprocess

def battery_status():
    try:
       comand = subprocess.run(
                  ["termux-battery-status"],
                  capture_output=True,
                  text=True,
                  check=True,
                  timeout=5
                )
       if comand.returncode == 0:
          return comand.stdout
       else:
          return comand.stderr
    except subprocess.TimeoutExpired:
           return "error timeout"
    except subprocess.CalledProcessError:
           return "comand error"
    except FileNotFoundError:
           return "Error Termux-api battery not found"
    except Exception as Error:
           return Error
