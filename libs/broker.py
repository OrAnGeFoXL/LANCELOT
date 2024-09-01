import os
from tinkoff.invest import *
from tinkoff.invest.utils import now
from datetime import timedelta
from typing import List


TOKEN = os.environ["INVEST_TOKEN"]

class CandlesSerial:
    def __init__(self, candles):
        self.open = [cast_money(i.open) for i in candles]
        self.high = [cast_money(i.high) for i in candles]
        self.low = [cast_money(i.low) for i in candles]
        self.close = [cast_money(i.close) for i in candles]
        self.volume = [i.volume for i in candles]

def get_history(figi: str, days: int = 10) -> List[HistoricCandle]:

    with Client(TOKEN) as cl:
        market_data: MarketDataService = cl.market_data
        history = market_data.get_candles(
            instrument_id=figi,
            from_=now() - timedelta(days=days),
            to=now(),
            interval=CandleInterval.CANDLE_INTERVAL_DAY
            ).candles
            
        return history

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
 
        ticker_dict = {}
        for method in ['shares', 'bonds', 'etfs' , 'currencies', 'futures']:
            for item in getattr(instruments, method)().instruments:
                if item.figi in TICKER:
                    figi_dict.update({item.ticker: item.figi})
                    
        return figi_dict

def figi_ticker(FIGI):
    """Получает тикер возвращает FIGI"""
    with Client(TOKEN) as cl:
        instruments: InstrumentsService = cl.instruments
        market_data: MarketDataService = cl.market_data
 
        figi_dict = {}
        for method in ['shares', 'bonds', 'etfs' , 'currencies', 'futures']:
            for item in getattr(instruments, method)().instruments:
                if item.figi in FIGI:
                    figi_dict.update({item.figi: item.ticker})
                    
        return figi_dict