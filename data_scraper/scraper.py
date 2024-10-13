from models import initialize_sql
from models.ticker import Ticker
from models.quote import Quote
from models.price_history import PriceHistory
from models.holding import Holding
from models.portfolio import Portfolio
from data_scraper.webclient import WebClient
from sqlalchemy.orm import sessionmaker

client = WebClient()
engine = initialize_sql()
Session = sessionmaker(bind=engine)

'''
Scrapes the tradable stock list from the API.
Goes through each result and either upadtes the existing ticker or adds a new one.
'''
def scrape_stock_list():
    stock_list = client.get_stock_list()
    print("found", len(stock_list), "stocks")
    session = Session()
        
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

    tickers = session.query(Ticker).all()
    for ticker in tickers[:50]:
        print(ticker)
    session.close()

# given a set of symbols, fetches the quote for each symbol and adds it to the database
def scrape_quotes(symbols, session=None):
    if not session: 
        session = Session()

    
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
    session.close()


# given a holding, fetches the price history and adds it to the database
def scrape_price_history(holding: Holding, end_date, start_date='2024-01-01', session=None):
    if not session:
        session = Session()
    
    price_history = client.get_price_history(holding.ticker_symbol, start_date, end_date)['historical']
    print('found', len(price_history), 'price history entries')

    # check if we have matching price history entries. Update if we do, add new ones if we don't
    for entry in price_history:
        existing_price_history = session.query(PriceHistory).filter_by(holding=holding, date=entry['date']).first()
        if existing_price_history:
            existing_price_history.open = entry['open']
            existing_price_history.high = entry['high']
            existing_price_history.low = entry['low']
            existing_price_history.close = entry['close']
            existing_price_history.volume = entry['volume']
            existing_price_history.change = entry['change']
            existing_price_history.change_percent = entry['changePercent']
        else:
            new_price_history = PriceHistory(symbol=holding.ticker_symbol, date=entry['date'],
                                            open=entry['open'], high=entry['high'], 
                                            low=entry['low'], close=entry['close'], 
                                            volume=entry['volume'], change=entry['change'], 
                                            change_percent=entry['changePercent'])
            new_price_history.holding = holding
            session.add(new_price_history)

    session.commit()
    session.close()