import pytest
from unittest.mock import patch
from models import Ticker, Quote, HistoricalPrice, Holding
from data_scraper.scraper import scrape_quotes, scrape_price_history, scrape_stock_list
from app import db

@patch('data_scraper.scraper.client')
def test_scrape_stock(mock_client, init_database):

    mock_client.get_stock_list.return_value = [
        {'symbol': 'AAPL', 'exchangeShortName': 'NASDAQ', 'name': 'Apple Inc.', 'type': 'Stock'},
        {'symbol': 'MSFT', 'exchangeShortName': 'NASDAQ', 'name': 'Microsoft Corp.', 'type': 'Stock'}
    ]
    
    scrape_stock_list()
    
    tickers = Ticker.query.all()
    assert len(tickers) == 2
    assert tickers[0].symbol == 'AAPL'
    assert tickers[1].symbol == 'MSFT'


@patch('data_scraper.scraper.client')
def test_scrape_quotes(mock_client, init_database):
    mock_client.get_quote.return_value = [
        {'symbol': 'AAPL', 'price': 150, 'volume': 1000},
        {'symbol': 'MSFT', 'price': 250, 'volume': 2000}
    ]
    
    ticker1 = Ticker(symbol='AAPL', exchange='NASDAQ', name='Apple Inc.', type='Stock')
    ticker2 = Ticker(symbol='MSFT', exchange='NASDAQ', name='Microsoft Corp.', type='Stock')
    db.session.add(ticker1)
    db.session.add(ticker2)
    db.session.commit()
    
    scrape_quotes(['AAPL', 'MSFT'])
    
    quotes = Quote.query.all()
    assert len(quotes) == 2
    assert quotes[0].ticker == ticker1
    assert quotes[0].price == 150
    assert quotes[0].volume == 1000
    assert quotes[1].ticker == ticker2
    assert quotes[1].price == 250
    assert quotes[1].volume == 2000

@patch('data_scraper.scraper.client')
def test_scrape_price_history(mock_client, init_database):
    mock_client.get_price_history.return_value = {
        'historical': [
            {'date': '2024-01-01', 'open': 100, 'high': 110, 'low': 90, 'close': 105, 'volume': 1000, 'change': 5, 'changePercent': 5},
            {'date': '2024-01-02', 'open': 105, 'high': 115, 'low': 95, 'close': 110, 'volume': 1500, 'change': 5, 'changePercent': 4.76}
        ]
    }
    ticker1 = Ticker(symbol='AAPL', exchange='NASDAQ', name='Apple Inc.', type='Stock')
    db.session.add(ticker1)
    db.session.commit()
    
    scrape_price_history(ticker1, start_date='2024-01-01', end_date='2024-01-02')
    
    price_histories = HistoricalPrice.query.all()
    assert len(price_histories) == 2
    assert price_histories[0].close == 105
    assert price_histories[1].close == 110