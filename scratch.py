from data_scraper.scraper import scrape_quotes, scrape_stock_list, scrape_price_history
from utilities import load_env_from_yaml
from models import Ticker, Quote, PriceHistory, Holding, Portfolio
from frontend.app import db

if __name__ == "__main__":
    load_env_from_yaml('env.yml')
    session = db.session

    # scrape_stock_list()
    tickers = session.query(Ticker).filter_by(type='N/A').all()
    for ticker in tickers:
        print(ticker)
    

    scrape_quotes(['AAPL', 'GOOG', 'MSFT', 'TSLA'], session=session)

    quotes = session.query(Quote).all()
    for quote in quotes:
        print(quote)
    

    portfolio = Portfolio()
    holding = Holding(session.query(Ticker).filter_by(symbol='AAPL').first(), session.query(Quote).filter_by(ticker_symbol='AAPL').first(), [], 10)
    portfolio.add_holding(holding)
    session.add(holding)
    session.commit()

    scrape_price_history(holding, start_date='2021-10-01', end_date='2021-10-10', session=session)
    #prices = session.query(PriceHistory).filter(PriceHistory.symbol == 'AAPL').all()
    #for price in prices:
    #   print(price)
    
    session.close()


