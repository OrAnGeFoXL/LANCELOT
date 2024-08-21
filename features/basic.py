
import pandas as pd
import math
from tinkoff.invest import *

import sys
import os
from typing import Union

from pprint import pprint

TOKEN = os.environ["INVEST_TOKEN"]

def cn(num: Union[float, int]) -> str:
    """
    Colorize a number, positive -> green, negative -> red, 0 -> no color.
    Args:
        num: The number to colorize.
    Returns:
        The colorized number as a string.
    """
    if isinstance(num, (float, int)):
        if num > 0:
            return f"\033[92m{num:.2f}\033[0m"  # зеленый цвет
        elif num < 0:
            return f"\033[91m{num:.2f}\033[0m"  # красный цвет
        else:
            return str(num)
    else:
        raise TypeError("Argument must be either int or float")

def draw_sparkline(values=[0, 1, 2, 3, 4, 5, 6, 7, 8, -8, -7, -6, -5, -4, -3, -2, -1, 0]):
    """
    Выводит sparkline из значений в List.
    """
    symbols = ' ▁▂▃▄▅▆▇█'

    max_value = max(values)
    scale = len(symbols) / max_value

    sparkline = ''
    for value in values:
        index = round(abs(value) * scale)

        if index >= len(symbols):
            index = len(symbols) - 1
        
        symbol = symbols[index]

        if value > 0:
            sparkline += f"\033[92m{symbol}\033[0m"
        elif value < 0:
            sparkline += f"\033[91m{symbol}\033[0m"
        else:
            sparkline += symbol
        
    print(sparkline)
    return sparkline


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

