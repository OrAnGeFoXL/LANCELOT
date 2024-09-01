import numpy as np
from typing import List, Union



#https://fin-plan.org/blog/investitsii/koeffitsient-sortino/
def sortino_ratio(returns: List[Union[float, int]], risk_free_rate: float, target_return: float) -> float:

    negative_returns = [r for r in returns if r < target_return]       #FIXME учесть нулевые значения
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