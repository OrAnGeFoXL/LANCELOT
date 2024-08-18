
import pandas as pd

from tinkoff.invest import *

import sys
import os
#current_dir = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(current_dir)

from pprint import pprint

TOKEN = os.environ["INVEST_TOKEN"]

def get_accs():
    with Client(TOKEN) as client:
        r = client.users.get_accounts()
        acc_list = [i.id for i in r.accounts if i.status == AccountStatus.ACCOUNT_STATUS_OPEN]
    return  acc_list

def cast_money(v):
    """
    https://tinkoff.github.io/investAPI/faq_custom_types/
    :param v:
    :return:
    """
    return v.units + v.nano / 1e9 # nano - 9 нулей

def get_portfolio_positions(account_id):
    """Запрашивает информацию о позиции в портфеле (get_positions)"""
    with Client(TOKEN) as cl:
        operations: OperationsService = cl.operations
        item = operations.get_portfolio(account_id=account_id)

        positions=item.positions
        pprint(positions)
    return 


def ticker_figi(TICKER):
    """Получает тикер возвращает FIGI"""
    with Client(TOKEN) as cl:
        instruments: InstrumentsService = cl.instruments
        market_data: MarketDataService = cl.market_data

        l = []
        for method in ['shares', 'bonds', 'etfs' , 'currencies', 'futures']:
            for item in getattr(instruments, method)().instruments:
                l.append({
                    'ticker': item.ticker,
                    'figi': item.figi,
                    'type': method,
                    'name': item.name,
                })

        df = DataFrame(l)
        df = df[df['ticker'] == TICKER]

        if df.empty:
            logger.error(f"Не найдено FIGI для {TICKER}")
            return ()

        figi=df['figi'].iloc[0]

        logger.success(f"Успешно найден figi {figi} для тикера {TICKER}")
    return (figi)

def figi_ticker(FIGI):
    """Получает тикер возвращает FIGI"""
    with Client(TOKEN) as cl:
        instruments: InstrumentsService = cl.instruments
        market_data: MarketDataService = cl.market_data
 
        l = []
        for method in ['shares', 'bonds', 'etfs' , 'currencies', 'futures']:
            for item in getattr(instruments, method)().instruments:
                l.append({
                    'ticker': item.ticker,
                    'figi': item.figi,
                    'type': method,
                    'name': item.name,
                })
 
        df = DataFrame(l)
 
        df = df[df['figi'] == FIGI]
        if df.empty:
            print(f"Нет тикера {FIGI}")
            return ()
 
        ticker=df['ticker'].iloc[0]
    return (ticker)

