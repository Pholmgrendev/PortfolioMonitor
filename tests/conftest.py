import pytest
from app import app, db
from models import Ticker, Quote, HistoricalPrice, Holding

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

@pytest.fixture(scope='function')
def init_database():
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()