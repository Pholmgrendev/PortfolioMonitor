from models import Base, TimestampMixin
from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship

'''
This class is a model for the portfolios table in the database. It has the following columns:
- id: The primary key of the table.
- total_value: The total value of the portfolio.'''
class Portfolio(Base, TimestampMixin):
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True)
    total_value = Column(Float, nullable=False, default=0)

    
    holdings = relationship("Holding", back_populates="portfolio", cascade="all, delete-orphan")
    
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