import os

from tinkoff.invest import Client
from simple_term_menu import TerminalMenu

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from pprint import pprint
from features import basic, obligation, portfolio
from basic import *
from libs.broker import *

TOKEN = os.environ["INVEST_TOKEN"]
ACCS = get_accs()


def test():
    with Client(TOKEN) as client:
        r = client.instruments.find_instrument(query="BBG001M2SC01")
        for i in r.instruments:
            pprint(i, indent=1)


def test_menu():
    options = ["Спарклайн", "Тест figi"]
    terminal_menu = TerminalMenu(options)

    match terminal_menu.show():
        case 0:
            basic.draw_sparkline([0, 1, 2, 3, 4, 5, 6, 7, 8, -8, -7, -6, -5, -4, -3, -2, -1, 0])
            for i in range(1, 50):
                basic.bar_chart(i, 100)
        case 1:
            basic.figi_ticker(["BBG000B9XRY4","BBG001M2SC01"])
   
def main():
    options = ["Облигации", "Проверка", "Список счётов (acount_id)", "Портфель"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()

    match menu_entry_index:
        case 0:
            obligation.show_obligation()
        case 1:
            test_menu()
        case 2:
            pprint(get_accs())
        case 3:
            portfolio.get_pf(ACCS[0])





if __name__ == "__main__":
    main()
