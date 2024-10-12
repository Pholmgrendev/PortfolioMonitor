from models import Base
from sqlalchemy import Column, Integer, String

'''
This class is a model for the tickers table in the database. It has the following columns:
- id: The primary key of the table.
- symbol: The symbol of the ticker.
- exchange: The exchange the ticker is listed on.
- name: The name of the ticker.
'''
class Ticker(Base):
    __tablename__ = 'tickers'
    symbol = Column(String, primary_key=True)
    exchange = Column(String, nullable=False)
    name = Column(String, nullable=False)


    def __init__(self, symbol, exchange, name):
        self.symbol = symbol
        self.exchange = exchange
        self.name = name
