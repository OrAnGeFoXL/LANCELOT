import os
from tinkoff.invest import *
from tinkoff.invest.utils import now
import numpy as np
from typing import List, Union
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

def sortino_ratio(returns: List[Union[float, int]], risk_free_rate: float, target_return: float) -> float:

    negative_returns = [r for r in returns if r < target_return]
    std_dev_negative_returns = np.std(negative_returns)
    sortino_ratio = (np.mean(returns) - risk_free_rate) / std_dev_negative_returns
    return sortino_ratio

def treynor_ratio(returns: List[Union[float, int]], risk_free_rate: float, beta: float) -> float:
    
    excess_returns = np.mean(returns) - risk_free_rate
    treynor_ratio = excess_returns / beta
    return treynor_ratio

def beta_coefficient(returns_portfolio: List[Union[float, int]], returns_market: List[Union[float, int]]) -> float:

    covariance_portfolio_market = np.cov(returns_portfolio, returns_market)[0, 1]
    variance_market = np.var(returns_market)
    beta_coefficient = covariance_portfolio_market / variance_market
    return beta_coefficient

def alpha_coefficient(returns_portfolio: List[Union[float, int]], returns_market: List[Union[float, int]], risk_free_rate: float, beta: float) -> float:

    mean_returns_portfolio = np.mean(returns_portfolio)
    mean_returns_market = np.mean(returns_market)
    alpha_coefficient = mean_returns_portfolio - (risk_free_rate + beta * (mean_returns_market - risk_free_rate))
    return alpha_coefficient

def sharpe_ratio(returns: List[Union[float, int]], risk_free_rate: float) -> float:

    mean_returns = np.mean(returns)
    std_returns = np.std(returns)
    sharpe_ratio = (mean_returns - risk_free_rate) / std_returns
    return sharpe_ratio

def sterling_ratio(max_drawdown: float, average_annual_return: float, risk_free_rate: float) -> float:

    sterling_ratio = (average_annual_return - risk_free_rate) / max_drawdown
    return sterling_ratio

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
                    orders_l += f"\033[41mSL\033[0m "
                if i.figi in tp_dict:
                    orders_l += f"\033[42mTP\033[0m "
                if i.figi in tst_dict:
                    orders_l += f"\033[41mTST\033[0m "

                print(f"----\033[93m{figi_dict.get(i.figi)}-{i.figi}\033[0m-------")
                print(f"{orders_l}(\033[94m{i.instrument_type}\033[0m) - {cn(cast_money(i.quantity))} шт. - {(cast_money(i.average_position_price_fifo))}")
                print(f"Доходность по цене: {cn(cast_money(i.expected_yield))} ({cn(pct_chng)}%)")
                bar_chart(pct_chng, cnf['limits']['weekly_pct'])
            else:
                if cnf['main']['show_blocked']:
                    print("---------------")
                    print(f"Актив заблокирован {figi_dict.get(i.figi)}-{i.figi}({i.instrument_type})")

