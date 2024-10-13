import pytest
from models import Ticker, Quote, HistoricalPrice, Holding, Portfolio
from app import db

def test_db_full(init_database):
    session = db.session

    # Create some tickers
    aapl = Ticker(symbol='dummy', exchange='NASDAQ', name='Apple Inc.', type='stock')
    goog = Ticker(symbol='tickers', exchange='NASDAQ', name='Alphabet Inc.', type='stock')
    msft = Ticker(symbol='nonexistant', exchange='NASDAQ', name='Microsoft Corporation', type='stock')
    tsla = Ticker(symbol='facimiles', exchange='NASDAQ', name='Tesla Inc.', type='stock')

    # Create some quotes
    aapl_quote = Quote(ticker=aapl, price=150.0, volume=1000)
    goog_quote = Quote(ticker=goog, price=2500.0, volume=2000)
    msft_quote = Quote(ticker=msft, price=300.0, volume=3000)
    tsla_quote = Quote(ticker=tsla, price=700.0, volume=4000)

    # Create some holdings
    aapl_holding = Holding(ticker=aapl, shares=10)
    goog_holding = Holding(ticker=goog, shares=20)
    msft_holding = Holding(ticker=msft, shares=30)
    tsla_holding = Holding(ticker=tsla, shares=40)

    # Create some price history
    aapl_price_history_1 = HistoricalPrice(ticker=aapl, date='2024-01-01', open=100.0, close=105.0, low=90.0, high=110.0, volume=1000, change=5.0, change_percent=5.0)
    aapl_price_history_2 = HistoricalPrice(ticker=aapl, date='2024-01-02', open=105.0, close=110.0, low=95.0, high=115.0, volume=1500, change=5.0, change_percent=4.76)

    portfolio = Portfolio(name='test')
    portfolio.holdings.append(aapl_holding)
    portfolio.holdings.append(goog_holding)
    portfolio.holdings.append(msft_holding)
    portfolio.holdings.append(tsla_holding)
    session.add(portfolio)
    session.commit()

    all_tickers= Ticker.query.all()
    assert len(all_tickers) == 4

    all_quotes = Quote.query.all()
    assert len(all_quotes) == 4

    all_holdings = Holding.query.all()
    assert len(all_holdings) == 4

    all_price_history = HistoricalPrice.query.all()
    assert len(all_price_history) == 2
    
    session.close()