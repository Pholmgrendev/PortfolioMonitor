from models import Base, TimestampMixin
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

'''
This class is a model for the holdings table in the database. It has the following columns:
- id: The primary key of the table.
- portfolio_id: The foreign key to the portfolios table.
- ticker_id: The foreign key to the tickers table.
- quote_id: The foreign key to the quotes table.
- shares: The number of shares of the stock.
- value: The value of the stock.
'''
class Holding(Base, TimestampMixin):
    __tablename__ = 'holdings'

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False)
    ticker_symbol = Column(Integer, ForeignKey('tickers.symbol'), nullable=False)
    quote_id = Column(Integer, ForeignKey('quotes.id'), nullable=False)
    shares = Column(Float, nullable=False)
    value = Column(Float, nullable=False)

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

    # __str__ should have the symbol, the shares, and the value
    def __str__(self):
        return f"{self.ticker.symbol} - Shares: {self.shares}, Value: {self.value}"
