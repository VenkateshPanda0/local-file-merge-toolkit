from colorama import Fore, Style, init


# Better terminal behavior
init(autoreset=True)


# ---------------------------------------------------------
# Basic Printers
# ---------------------------------------------------------

def print_header(text: str) -> None:
    """Print styled section header."""
    width = max(len(text) + 4, 32)
    line = "=" * width

    print(f"\n{Fore.CYAN}{line}")
    print(f"  {text}")
    print(f"{line}{Style.RESET_ALL}")


def print_success(text: str) -> None:
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")


def print_warning(text: str) -> None:
    print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")


def print_error(text: str) -> None:
    print(f"{Fore.RED}{text}{Style.RESET_ALL}")


def print_info(text: str) -> None:
    print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")


# ---------------------------------------------------------
# Menu
# ---------------------------------------------------------

def prompt_menu(title: str, options: dict[str, str]) -> str:
    """
    Display menu and return valid user choice.
    Handles invalid input safely.
    """

    while True:
        print_header(title)

        for key, value in options.items():
            print(f"{Fore.CYAN}[{key}] {value}{Style.RESET_ALL}")

        print()

        try:
            choice = input("Select an option: ").strip()

        except KeyboardInterrupt:
            print()
            print_warning("Operation cancelled.")
            return "0"

        except EOFError:
            print()
            print_warning("Input closed.")
            return "0"

        if choice in options:
            return choice

        print_error("Invalid choice. Try again.")