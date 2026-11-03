import subprocess 

def info_battery():
  resultado = subprocess.run(
    ["termux-battery-status"],
    capture_output=True,
    text=True 
  )
  return resultado.stdout
