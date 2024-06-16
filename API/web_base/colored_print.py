

from colorama import Fore, Style, init
init(autoreset=True)

def print_colored(text, color):
    """
    Print text in a specified color.

    :param text: The text to print.
    :type text: str
    :param color: The color to print the text in.
    :type color: str
    """
    color_dict = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE
    }
    print(color_dict.get(color.lower(), Fore.WHITE) + text)