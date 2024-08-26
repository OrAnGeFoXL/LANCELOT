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

        orders: StopOrdersService = cl.stop_orders
        stop_orders = orders.get_stop_orders(account_id=account_id).stop_orders

        sl_dict = {}
        tp_dict = {}
        tst_dict = {}

        for i in stop_orders:

            if i.order_type == StopOrderType.STOP_ORDER_TYPE_STOP_LOSS:
                sl_dict.update({i.figi: i.lots_requested})

            elif i.order_type == StopOrderType.STOP_ORDER_TYPE_TAKE_PROFIT:
                tp_dict.update({i.figi: i.lots_requested})
              
        
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

        figi_list = [position.figi for position in positions]
        figi_dict = figi_ticker(figi_list)
        
        for i in positions: 
            if i.blocked == False:
                size = cast_money(i.quantity)*cast_money(i.average_position_price_fifo)
                pct_chng = 100*cast_money(i.expected_yield)/size

                orders_l = ''
                if i.figi in sl_dict:
                    orders_l += f"\033[41mSL\033[0m"
                if i.figi in tp_dict:
                    orders_l += f"\033[42mTP\033[0m"
                if i.figi in tst_dict:
                    orders_l += f"\033[41mTST\033[0m"

                print(cast_money(i.average_position_price_fifo))

                print(f"{orders_l}{figi_dict.get(i.figi)}-{i.figi}({i.instrument_type}) - {cn(cast_money(i.quantity))} шт. - {cn(cast_money(i.expected_yield))} {(cast_money(i.average_position_price_fifo))}")
                print(f"Доходность по цене: {cn(cast_money(i.expected_yield))} ({cn(pct_chng)}%)")
                bar_chart(pct_chng, cnf['limits']['weekly_pct'])
            else:
                if cnf['main']['show_blocked']:
                    print(f"Актив заблокирован {figi_dict.get(i.figi)}-{i.figi}({i.instrument_type})")

