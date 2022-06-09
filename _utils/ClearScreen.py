from os import name,system

def clear_screen():
    """
    Clear command window to log progress.
    """

    # Windows
    if name == 'nt':
        _ = system('cls')

    # Max and Linux
    else:
        _ = system('clear')

    return