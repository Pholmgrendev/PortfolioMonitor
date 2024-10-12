from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

'''
This function initializes the SQL database and returns the engine.
It's a bit janky because of the way that each table is defgined in a separate file.
Created it by following these instructions: 
https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/database/sqlalchemy.html#importing-all-sqlalchemy-models
'''
def initialize_sql():
    engine = create_engine('sqlite:///portfolio_monitor.db')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    return engine