from models import Ticker, Quote, HistoricalPrice, Holding, Portfolio
from data_scraper.webclient import WebClient
from app import db

client = WebClient()

'''
Scrapes the tradable stock list from the API.
Goes through each result and either upadtes the existing ticker or adds a new one.
'''
def scrape_stock_list():
    stock_list = client.get_stock_list()
    print("found", len(stock_list), "stocks")
    session = db.session
        
    for stock in stock_list:
        existing_ticker = session.query(Ticker).filter_by(symbol=stock['symbol']).first()
        if existing_ticker:
            existing_ticker.exchange = stock['exchangeShortName']
            existing_ticker.name = stock['name']
            existing_ticker.type = stock['type']
        else:
            new_ticker = Ticker(symbol=stock['symbol'], exchange=stock['exchangeShortName'] or 'N/A', name=stock['name'] or 'N/A', type=stock['type'] or 'N/A')
            session.add(new_ticker)
    session.commit()


# given a set of symbols, fetches the quote for each symbol and adds it to the database
def scrape_quotes(symbols):
    session = db.session
    
    quotes = client.get_quote(symbols)
    print('found', len(quotes), 'quotes')
    for quote in quotes:
        symbol = quote['symbol']
        ticker = session.query(Ticker).filter_by(symbol=symbol).first()
        if ticker:
            existing_quote = session.query(Quote).filter_by(ticker=ticker).first()
            if existing_quote:
                existing_quote.price = quote['price']
                existing_quote.volume = quote['volume']
            else:
                new_quote = Quote(ticker=ticker, price=quote['price'], volume=quote['volume'])
                session.add(new_quote)
    session.commit()


# given a holding, fetches the price history and adds it to the database
def scrape_price_history(ticker: Ticker, end_date, start_date='2024-01-01'):
    session = db.session

    price_history = client.get_price_history(ticker.symbol, start_date, end_date)['historical']
    print('found', len(price_history), 'price history entries')

    # check if we have matching price history entries. Update if we do, add new ones if we don't
    for entry in price_history:
        existing_price_history = session.query(HistoricalPrice).filter_by(ticker=ticker, date=entry['date']).first()
        if existing_price_history:
            existing_price_history.open = entry['open']
            existing_price_history.high = entry['high']
            existing_price_history.low = entry['low']
            existing_price_history.close = entry['close']
            existing_price_history.volume = entry['volume']
            existing_price_history.change = entry['change']
            existing_price_history.change_percent = entry['changePercent']
        else:
            new_price_history = HistoricalPrice(ticker=ticker, date=entry['date'], 
                                                open=entry['open'], high=entry['high'], 
                                                low=entry['low'], close=entry['close'], 
                                                volume=entry['volume'], change=entry['change'], 
                                                change_percent=entry['changePercent'])
            session.add(new_price_history)

    session.commit()
