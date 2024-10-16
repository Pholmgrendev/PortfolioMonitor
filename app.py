from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots
import plotly.graph_objs as go

from utilities import load_env_from_yaml
from models import db
from models import Portfolio, Holding, Ticker, Quote, HistoricalPrice
from data_analyzer.analyzer import analyze_portfolio
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

# initialize some of our DB tables
with app.app_context():
    startup()

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
        if not ticker.historical_prices:
            populate_price_history(ticker)
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


@app.route('/price_history/<int:ticker_id>')
def price_history(ticker_id):
    ticker = Ticker.query.get(ticker_id)
    if not ticker:
        flash("Error: Ticker not found.", 'error')
        return redirect(url_for('index'))
    
    price_history = HistoricalPrice.query.filter_by(ticker_id=ticker_id).order_by(HistoricalPrice.date.desc()).all()
    if not price_history:
        print('No price history found, scraping...')

        price_history = populate_price_history(ticker_id)
        
    return render_template('price_history.html', ticker=ticker, price_history=price_history)


@app.route('/advanced_stats')
def advanced_stats():
    stats = analyze_portfolio()

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=stats['dates'], y=stats['cumulative_returns'], mode='lines', name='Cumulative Returns'))
    graph_html = fig.to_html(full_html=False)
    return render_template('advanced_stats.html', stats=stats, graph_html=graph_html)


def populate_price_history(ticker):
    today = date.today()
    five_years_ago = today - relativedelta(years=5)
    today_formatted = today.strftime('%Y-%m-%d')
    five_years_ago_formatted = five_years_ago.strftime('%Y-%m-%d')
        
    scrape_price_history(ticker, start_date=five_years_ago_formatted, end_date=today_formatted)
    price_history = HistoricalPrice.query.filter_by(ticker_id=ticker.id).order_by(HistoricalPrice.date.desc()).all()
    return price_history


if __name__ == '__main__':
    app.run(debug=True)
    
    