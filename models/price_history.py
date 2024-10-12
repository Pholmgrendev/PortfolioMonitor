from models import Base, TimestampMixin
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

'''
This class is a model for the price_history table in the database. It has the following columns:
- id: The primary key of the table.
- symbol: The symbol of the stock.
- date: The date of the price.
- open: The opening price of the stock.
- high: The highest price of the stock.
- low: The lowest price of the stock.
- close: The closing price of the stock.
- volume: The volume of the stock.
- change: The change in price.
- change_percent: The percentage change in price.
'''
class PriceHistory(Base, TimestampMixin):
    __tablename__ = 'price_history'

    id = Column(Integer, primary_key=True)
    holding_id = Column(Integer, ForeignKey('holdings.id'), nullable=False)
    symbol = Column(String, nullable=False)
    date = Column(String, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    change = Column(Float, nullable=False)
    change_percent = Column(Float, nullable=False)

    # add a relationship to the Holding table
    holding = relationship("Holding", back_populates="price_history_list")


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
