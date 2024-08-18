import os

from tinkoff.invest import Client
from simple_term_menu import TerminalMenu

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from pprint import pprint
from features import basic, obligation
from basic import *


TOKEN = os.environ["INVEST_TOKEN"]
ACCS = basic.get_accs()


def test():
    with Client(TOKEN) as client:
        r = client.instruments.find_instrument(query="BBG001M2SC01")
        for i in r.instruments:
            pprint(i, indent=1)


def main():
    options = ["Облигации", "Проверка", "Список счётов (acount_id)"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()

    match menu_entry_index:
        case 0:
            obligation.show_obligation()
        case 1:
            test()
        case 2:
            pprint(basic.get_accs())

    print(f"You have selected {options[menu_entry_index]}!")



if __name__ == "__main__":
    main()
