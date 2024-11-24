from colorama import Fore

import inspect

def print_function_name(func):
    def wrapper(*args, **kwargs):
        stack_depth = len(inspect.stack()) - 1  # Subtract 1 to exclude the current function
        indentation = "    " * stack_depth  # Four spaces per depth level
        print(f"{indentation}{Fore.GREEN}->{Fore.RESET} {func.__name__} {Fore.BLUE}↓{Fore.RESET}")
        result = func(*args, **kwargs)
        return result
    return wrapper