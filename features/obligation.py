import os
from tinkoff.invest import *
from tinkoff.invest.utils import now
from pprint import pprint

from basic import cast_money, get_accs, cn

from simple_term_menu import TerminalMenu

from datetime import timedelta 
import time


TOKEN = os.environ["INVEST_TOKEN"]

def show_obligation():

    options = ["Общий список облигаций по счетам", "Купонная доходность за день"]
    terminal_menu = TerminalMenu(options)

    match terminal_menu.show():
        case 0:
            for account_id  in get_accs():
                print(f"\033[92mСчёт: {account_id}\033[0m")
                get_obligation(account_id)
        case 1:
            for account_id  in get_accs():
                print(f"\033[92mСчёт: {account_id}\033[0m")
                daily_bond_yield(account_id)


def get_obligation(account_id):
    """Запрашивает информацию об облигациях на счету"""
    with Client(TOKEN) as cl:
        operations: OperationsService = cl.operations
        item = operations.get_portfolio(account_id=account_id)

        positions=item.positions
        position:PortfolioPosition = next((position for position in positions if position.instrument_type == 'bond'), None)
        
        bond_list = [position for position in positions if position.instrument_type == 'bond']

        if not bond_list:
            print(f"Нет облигаций на счёте {account_id}.")
        else:
            for bond in bond_list:           

                lot_yield = cast_money(bond.expected_yield)     #доходность всей позиции
                lots_qty = int(cast_money(bond.quantity_lots))

                price = cast_money(bond.current_price)

                pct_yield = (lot_yield / (price*lots_qty))*100

                nkd_yield = cast_money(bond.current_nkd)*lots_qty
                nkd_pct_yield = (cast_money(bond.current_nkd) / price)*100

                print(f"\033[93m{bond.figi}\033[0m")
                print(f"Количество лотов: {lots_qty}")
                print(f"Текущая цена: {price:.2f} {bond.current_price.currency}" )
                print(f"Доходность по цене: {cn(lot_yield)} ({cn(pct_yield)}%)")
                print(f"Доходность по купону: {cn(nkd_yield)} ({cn(nkd_pct_yield)}%)")
                #print('\n')        
    return 

def instrumemt_info(figi)->Instrument:
    with Client(TOKEN) as cl:
        instruments: InstrumentsService = cl.instruments
        market_data: MarketDataService = cl.market_data
        item = instruments.get_instrument_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi).instrument
        #pprint(item, indent=4)
    return item

def daily_bond_yield(account_id):

    with Client(TOKEN) as cl:
        operations: OperationsService = cl.operations
        item = operations.get_portfolio(account_id=account_id)

        positions=item.positions
        position:PortfolioPosition = next((position for position in positions if position.instrument_type == 'bond'), None)
        
        bond_list = [position for position in positions if position.instrument_type == 'bond']
        lots_qty = {position.figi: position.quantity_lots for position in bond_list}

        if not bond_list:
            print(f"Нет облигаций на счёте {account_id}.")
        else:
            for bond in bond_list:           
                instruments: InstrumentsService = cl.instruments              
                
                coupon = instruments.get_bond_coupons(figi=bond.figi,
                                                    from_=now(),
                                                    to=now() + timedelta(days=365)
                                                    ).events                             
                if not coupon:
                    print(f"Нет информации но купонам {bond.figi}.")
                else:
                    coupon = coupon[-1] #только самый свежий купон
                
                    qty = cast_money(lots_qty[bond.figi]) 
                    coupon_size = cast_money(coupon.pay_one_bond)
                    period = coupon.coupon_period
                    daily_yield = qty * coupon_size / period

                    print(f"\033[93m{bond.figi}\033[0m")
                    print(f"Размер купона: {coupon_size:.2f} {coupon.pay_one_bond.currency}" )
                    print(f"Доходность в день по купону: {cn(daily_yield)} {coupon.pay_one_bond.currency}")
