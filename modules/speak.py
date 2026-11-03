import subprocess

def text_speak(data):
    try:
      comand = subprocess.run(
                  ["termux-tts-speak", data],
                  capture_output=True,
                  text=True,
                  check=True,
                  timeout=5
               )
      if comando.returncode == 0:
         return comand.stdout
      else:
         return comand.stderr
    except subprocess.CalledProcessError:
         return "error comand failed"
    except subprocess.TimeoutExpired:
         return "error timeout"
    except FileNotFoundError:
         return "not found termux-api"
    except Exception as Error:
         return Error

