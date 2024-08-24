import os
from tinkoff.invest import *
from tinkoff.invest.utils import now
from pprint import pprint

from basic import cast_money, get_accs, cn, figi_ticker, bar_chart

from simple_term_menu import TerminalMenu

from datetime import timedelta 
import time

import toml
with open('config.toml') as f:
    cnf = toml.load(f)
#print(data)

TOKEN = os.environ["INVEST_TOKEN"]

def get_pf(account_id):
    """Запрашивает информацию об активах на счету"""
    with Client(TOKEN) as cl:
        operations: OperationsService = cl.operations
        item = operations.get_portfolio(account_id=account_id)
        
        #Общая информация по портфелю
        print(*[f"Общая сумма {k}: {cn(cast_money(v))} {v.currency}" for k, v in {
            'акций': item.total_amount_shares,
            'облигаций': item.total_amount_bonds,
            'ETF': item.total_amount_etf,
            'валют': item.total_amount_currencies,
            'фьючерсов': item.total_amount_futures,
            'опционов': item.total_amount_options,
            'структурных нот': item.total_amount_sp,
            'портфеля': item.total_amount_portfolio
        }.items() if (v.units != 0 or v.nano != 0)], sep='\n')

        positions=item.positions
        
        for i in positions: 
            if i.blocked == False:
                size = cast_money(i.quantity)*cast_money(i.average_position_price_fifo)
                pct_chng = 100*cast_money(i.expected_yield)/size

                print(f"{figi_ticker(i.figi)}({i.instrument_type}) - {cn(cast_money(i.quantity))} шт. - {cn(cast_money(i.expected_yield))} {cn(cast_money(i.average_position_price))}")
                print(f"Доходность по цене: {cn(cast_money(i.expected_yield))} ({cn(pct_chng)}%)")
                bar_chart(pct_chng, cnf['limits']['weekly_pct'])
            else:
                print(f"Актив заблокирован {figi_ticker(i.figi)}({i.instrument_type})")