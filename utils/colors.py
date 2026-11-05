from colorama import Fore

def info(msg: str) -> str:
    return f"{Fore.RED}[+] {Fore.YELLOW}{msg}{Fore.RESET}"
