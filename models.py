from app import db
from sqlalchemy.sql import func

class Ticker(db.Model):
    __tablename__ = 'tickers'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    exchange = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)

    quote = db.relationship('Quote', uselist=False, backref='ticker', lazy=True)
    historical_prices = db.relationship('HistoricalPrice', backref='ticker', lazy=True)
    holding = db.relationship('Holding', uselist=False, backref='ticker', lazy=True)


class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    ticker_id = db.Column(db.Integer, db.ForeignKey('tickers.id'), nullable=False, unique=True)


class HistoricalPrice(db.Model):
    __tablename__ = 'historical_prices'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    open = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    change = db.Column(db.Float, nullable=False)
    change_percent = db.Column(db.Float, nullable=False)
    ticker_id = db.Column(db.Integer, db.ForeignKey('tickers.id'), nullable=False)


class Holding(db.Model):
    __tablename__ = 'holdings'
    id = db.Column(db.Integer, primary_key=True)
    shares = db.Column(db.Integer, nullable=False)
    ticker_id = db.Column(db.Integer, db.ForeignKey('tickers.id'), nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=True)


class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    holdings = db.relationship('Holding', backref='portfolio', lazy=True)

    @property
    def total_value(self):
        return sum(holding.shares * holding.ticker.quote.price for holding in self.holdings if holding.ticker.quote)