from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import initialize_sql
from models.ticker import Ticker, Base
from models.quote import Quote
from models.holding import Holding
from models.price_history import PriceHistory
from models.portfolio import Portfolio

if __name__ == '__main__':
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    engine = initialize_sql()

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Create some tickers
    aapl = Ticker(symbol='AAPL', exchange='NASDAQ', name='Apple Inc.')
    goog = Ticker(symbol='GOOG', exchange='NASDAQ', name='Alphabet Inc.')
    msft = Ticker(symbol='MSFT', exchange='NASDAQ', name='Microsoft Corporation')
    tsla = Ticker(symbol='TSLA', exchange='NASDAQ', name='Tesla Inc.')

    # Create some quotes
    aapl_quote = Quote(ticker=aapl, price=150.0, volume=1000)
    goog_quote = Quote(ticker=goog, price=2500.0, volume=2000)
    msft_quote = Quote(ticker=msft, price=300.0, volume=3000)
    tsla_quote = Quote(ticker=tsla, price=700.0, volume=4000)

    # Create some holdings
    aapl_holding = Holding(ticker=aapl, quote=aapl_quote, price_history_list=[], shares=10)
    fake_holding = Holding(ticker=aapl, quote=goog_quote, price_history_list=[], shares=50)
    goog_holding = Holding(ticker=goog, quote=goog_quote, price_history_list=[], shares=20)
    msft_holding = Holding(ticker=msft, quote=msft_quote, price_history_list=[], shares=30)
    tsla_holding = Holding(ticker=tsla, quote=tsla_quote, price_history_list=[], shares=40)

    # Create some price history
    aapl_price_history_1 = PriceHistory(symbol='AAPL', date='2021-01-01', open=100.0, high=200.0, low=50.0, close=150.0, volume=1000, change=50.0, change_percent=0.33)
    aapl_price_history_2 = PriceHistory(symbol='AAPL', date='2021-01-02', open=150.0, high=250.0, low=100.0, close=200.0, volume=2000, change=50.0, change_percent=0.25)

    # Add the price history to the holding
    aapl_holding.price_history_list.append(aapl_price_history_1)
    aapl_holding.price_history_list.append(aapl_price_history_2)

    portfolio = Portfolio()

    # Add the holdings to the portfolio
    portfolio.add_holding(aapl_holding)
    portfolio.add_holding(fake_holding)
    portfolio.add_holding(goog_holding)
    portfolio.add_holding(msft_holding)
    portfolio.add_holding(tsla_holding)

    # Add the tickers to the session
    session.add(aapl)
    session.add(goog)
    session.add(msft)
    session.add(tsla)

    # Add the quotes to the session
    session.add(aapl_quote)
    session.add(goog_quote)
    session.add(msft_quote)
    session.add(tsla_quote)

    session.add(portfolio)
    # Commit the session
    session.commit()

    print('Database setup complete.')

    #query the database
    print('Querying the database...')
    holdings = session.query(Holding).all()
    print('number of holdings found: ' + str(len(holdings)))
    for holding in holdings:
        print(holding)
        if holding.price_history_list:
            for price_history in holding.price_history_list:
                print(price_history)
    
    # clear out all the tables
    session.query(PriceHistory).delete()
    session.query(Holding).delete()
    session.query(Portfolio).delete()
    session.query(Quote).delete()
    session.query(Ticker).delete()
    session.commit()

    session.close()
    print('DB setup complete, database cleared.')