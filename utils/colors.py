from colorama import init, Fore 

init(autoreset=True)

def info(msg: str) -> str:
    return f"{Fore.RED}[+] {Fore.YELLOW}{msg}{Fore.RESET}"
