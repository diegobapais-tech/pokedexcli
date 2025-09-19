from colorama import Fore, Style, init
import readline

init(autoreset=True)

def std_command_output(message):
    print(Fore.BLUE + message)

def success_command_output(message):
    print(Fore.GREEN + message)

def warning_command_output(message):
    print(Fore.YELLOW + message)

def error_command_output(message):
    print(Fore.RED + message)

def std_command_input(message):
    return input(Fore.RED + Style.BRIGHT + message + Fore.WHITE + Style.NORMAL) 


