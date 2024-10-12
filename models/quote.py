from models import Base, TimestampMixin
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

'''
This class is a model for the quotes table in the database. It has the following columns:
- id: The primary key of the table.
- ticker: The symbol of the ticker.
- price: The price of the ticker.
- volume: The volume of the ticker.
'''
class Quote(Base, TimestampMixin):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    ticker_symbol = Column(Integer, ForeignKey('tickers.symbol'), nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

    ticker = relationship("Ticker")


    def __init__(self, ticker, price, volume):
        self.ticker = ticker
        self.price = price
        self.volume = volume
    

    def __str__(self):
        return f"{self.ticker} - Price: {self.price}, Volume: {self.volume}"
