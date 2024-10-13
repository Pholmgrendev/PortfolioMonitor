from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from utilities import load_env_from_yaml
from models import db
from models import Portfolio, Holding, Ticker, Quote, HistoricalPrice
from data_scraper.scraper import scrape_stock_list, scrape_quotes, scrape_price_history
from data_scraper.scraper import startup, update_portfolio_quotes

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

load_env_from_yaml('env.yaml')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'  # Example using SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'itsasecret'

db.init_app(app)
with app.app_context():
    db.create_all()

scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_stock_list, trigger='interval', minutes=60)
scheduler.add_job(func=update_portfolio_quotes, trigger='interval', minutes=30)
scheduler.start()


@app.route('/')
def index():
    portfolio = Portfolio.query.first()  # Assuming a single portfolio for simplicity
    holdings = portfolio.holdings
    return render_template('portfolio.html', portfolio=portfolio, holdings=holdings)


@app.route('/add_holding', methods=['POST'])
def add_holding():
    symbol = request.form['symbol']
    shares = int(request.form['shares'])
    ticker = Ticker.query.filter_by(symbol=symbol).first()
    portfolio = Portfolio.query.first()
    if ticker:
        holding = Holding.query.filter_by(ticker=ticker,portfolio=portfolio).first()
        if holding:
            flash(f"Holding for {symbol} already exists", 'error')
            return redirect(url_for('index'))
        if not ticker.quote:
            scrape_quotes([symbol])
        try:
            holding = Holding(ticker=ticker, shares=shares, portfolio=portfolio)
            db.session.add(holding)
            db.session.commit()
        except Exception as e:
            flash(f"Error: {str(e)}", 'error')
    else:
        flash(f"Error: Ticker {symbol} not found", 'error')
    return redirect(url_for('index'))


@app.route('/remove_holding/<int:holding_id>', methods=['POST'])
def remove_holding(holding_id):
    holding = Holding.query.get(holding_id)
    if holding:
        db.session.delete(holding)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit_holding/<int:holding_id>', methods=['POST'])
def edit_holding(holding_id):
    holding = Holding.query.filter_by(id=holding_id).first()
    shares = int(request.form['shares'])
    if shares <= 0:
        flash("Error: Shares must be greater than 0.", 'error')
        return redirect(url_for('index'))
    if holding:
        holding.update_shares(shares)
        db.session.commit()
        flash(f"Holding for {holding.ticker.symbol} updated successfully.", 'success')
    else:
        flash("Error: Holding not found.", 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        startup()
    app.run(debug=True)
    
    