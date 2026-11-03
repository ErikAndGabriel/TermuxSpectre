import subprocess

def notification(title, text):
    try:
       comand = subprocess.run(
                [
                   "termux-notfication",
                   "--title", title,
                   "--content", text
                ],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
       )

       if comand.returncode == 200:
           return comand.stdout
       else:
           return comand.stderr
    except subprocess.TimeoutExpired:
           return "error timeout"
    except FileNotFoundError:
           return "error comand not found"
    except CalledProcessError:
           return "Error comand failed"
    except Exception as Error:
           return Error
