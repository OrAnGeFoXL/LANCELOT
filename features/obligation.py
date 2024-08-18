import os
from tinkoff.invest import *
from pprint import pprint

from basic import cast_money, get_accs

TOKEN = os.environ["INVEST_TOKEN"]

def show_obligation():
    for account_id  in get_accs():
        print(f"\033[92mСчёт: {account_id}\033[0m")
        get_obligation(account_id)

def get_obligation(account_id):
    """Запрашивает информацию об облигациях на счету"""
    with Client(TOKEN) as cl:
        operations: OperationsService = cl.operations
        item = operations.get_portfolio(account_id=account_id)

        positions=item.positions
        position:PortfolioPosition = next((position for position in positions if position.instrument_type == 'bond'), None)
        
        bond_list = [position for position in positions if position.instrument_type == 'bond']

        if not bond_list:
            print("Нет облигаций на счёте {account_id}.")
        else:
            for bond in bond_list:           

                lot_yield = cast_money(bond.expected_yield)
                lots_qty = int(cast_money(bond.quantity_lots))

                price = cast_money(bond.current_price)

                pos_yield = lot_yield * lots_qty
                pct_yield = (pos_yield / price)*100

                nkd_yield = cast_money(bond.current_nkd)*lots_qty
                nkd_pct_yield = (cast_money(bond.current_nkd) / price)*100

                print(f"\033[93m{bond.figi}\033[0m")
                print(f"Количество лотов: {lots_qty}")
                print(f"Текущая цена: {price:.2f} {bond.current_price.currency}" )
                print(f"Доходность по цене: {lot_yield:.2f} ({pct_yield:.2f}%)")
                print(f"Доходность по купону: {nkd_yield:.2f} ({nkd_pct_yield:.2f}%)")
                #print('\n')        
    return 
