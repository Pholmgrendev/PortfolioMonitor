from frontend.app import db
from sqlalchemy.sql import func

class Ticker(db.Model):
    __tablename__ = 'tickers'
    symbol = db.Column(db.String, primary_key=True)
    exchange = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, symbol, exchange, name, type):
        self.symbol = symbol
        self.exchange = exchange
        self.name = name
        self.type = type

    def __str__(self):
        return f"{self.symbol} - {self.name} ({self.exchange})"
   

class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    ticker_symbol = db.Column(db.String, db.ForeignKey('tickers.symbol'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    change = db.Column(db.Float, nullable=False)
    change_percent = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    ticker = db.relationship("Ticker")

    def __init__(self, ticker_symbol, price, change, change_percent):
        self.ticker_symbol = ticker_symbol
        self.price = price
        self.change = change
        self.change_percent = change_percent

    def __str__(self):
        return f"{self.ticker_symbol} - Price: {self.price}, Change: {self.change}, Change Percent: {self.change_percent}"


class PriceHistory(db.Model):
    __tablename__ = 'price_history'
    id = db.Column(db.Integer, primary_key=True)
    holding_id = db.Column(db.Integer, db.ForeignKey('holdings.id'), nullable=False)
    symbol = db.Column(db.String, db.ForeignKey('tickers.symbol'), nullable=False)
    date = db.Column(db.String, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    change = db.Column(db.Float, nullable=False)
    change_percent = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    holding = db.relationship("Holding", back_populates="price_history_list")
    ticker = db.relationship("Ticker")

    def __init__(self, symbol, date, open, high, low, close, volume, change, change_percent):
        self.symbol = symbol
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.change = change
        self.change_percent = change_percent

    def __str__(self):
        return f"{self.symbol} - Date: {self.date}, Open: {self.open}, High: {self.high}, Low: {self.low}, Close: {self.close}, Volume: {self.volume}, Change: {self.change}, Change Percent: {self.change_percent}"


class Holding(db.Model):
    __tablename__ = 'holdings'
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    ticker_symbol = db.Column(db.String, db.ForeignKey('tickers.symbol'), nullable=False)
    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id'), nullable=False)
    shares = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    portfolio = relationship("Portfolio", back_populates="holdings")
    ticker = relationship("Ticker")
    quote = relationship("Quote")
    price_history_list = relationship("PriceHistory", back_populates="holding", cascade="all, delete-orphan")

    def __init__(self, ticker, quote, price_history_list, shares):
        self.ticker = ticker
        self.quote = quote
        self.price_history_list = price_history_list
        self.shares = shares
        self.value = shares * quote.price

    # whenever we update the shares, we need to update the value
    def update_shares(self, shares):
        self.shares = shares
        self.value = shares * self.quote.price

    # whenever we update the quote, we need to update the value
    def update_quote(self, quote):
        self.quote = quote
        self.value = self.shares * quote.price

    def __str__(self):
        return f"{self.ticker.symbol} - Shares: {self.shares}, Value: {self.value}"


# portfolio containing a list of holdings and a total value of the portfolio
class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    id = db.Column(db.Integer, primary_key=True)
    total_value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    holdings = db.relationship("Holding", back_populates="portfolio", cascade="all, delete-orphan")

    def __init__(self):
        self.holdings = []
        self.total_value = 0

    def add_holding(self, holding):
        self.holdings.append(holding)
        self.total_value += holding.value

    def remove_holding(self, holding):
        self.holdings.remove(holding)
        self.total_value -= holding.value

    def update_holding_shares(self, holding, shares):
        holding.update_shares(shares)
        self.total_value = sum([holding.value for holding in self.holdings])

    def update_holding_quote(self, holding, quote):
        holding.update_quote(quote)
        self.total_value = sum([holding.value for holding in self.holdings])

    def __str__(self):
        return f"Portfolio Value: {self.total_value}, Holdings: {self.holdings}"
