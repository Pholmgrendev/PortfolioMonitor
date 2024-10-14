from flask import jsonify, request
from models import db
from models import Portfolio, Holding, Ticker, Quote, HistoricalPrice
import pandas as pd
import numpy as np

def calculate_daily_returns(holdings, dates):
    portfolio_values = []
    for date in dates:
        total_value = 0
        for holding in holdings:
            price = HistoricalPrice.query.filter_by(ticker=holding.ticker, date=date).first()
            total_value += price.close * holding.shares
        portfolio_values.append(total_value)
    daily_returns = pd.Series(portfolio_values).pct_change().dropna()
    return daily_returns


def calculate_cumulative_returns(daily_returns):
    return daily_returns.cumsum()


def calculate_volatility(daily_returns):
    return np.std(daily_returns)

# current risk free rate is 4.08%
def calculate_sharpe_ratio(daily_returns, volatility, risk_free_rate=0.0408):
    excess_returns = daily_returns - risk_free_rate / 252  # Assuming 252 trading days in a year
    mean_excess_return = np.mean(excess_returns)
    sharpe_ratio = mean_excess_return / volatility
    return sharpe_ratio


def calculate_asset_allocation(holdings):
    total_holdings = len(holdings)
    stocks = [holding.ticker.type == 'stock' for holding in holdings].count(True) / total_holdings
    bonds = [holding.ticker.type == 'bond' for holding in holdings].count(True) / total_holdings
    etfs = [holding.ticker.type == 'etf' for holding in holdings].count(True) / total_holdings
    return {"asset_allocation": {"stocks": stocks, "bonds": bonds, "etfs": etfs}}

def analyze_portfolio():
    portfolio = db.session.query(Portfolio).first()
    holdings = portfolio.holdings
    dates = sorted(set(price.date for price in holdings[0].ticker.historical_prices))
    
    daily_returns = calculate_daily_returns(holdings, dates)
    cumulative_returns = calculate_cumulative_returns(daily_returns)
    volatility = calculate_volatility(daily_returns)
    sharpe_ratio = calculate_sharpe_ratio(daily_returns, volatility)
    asset_allocation = calculate_asset_allocation(holdings)
    
    result = {
        "dates": dates,
        "cumulative_returns": cumulative_returns,
        "volatility": volatility,
        "sharpe_ratio": sharpe_ratio,
        "asset_allocation": asset_allocation
    }

    return result