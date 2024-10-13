from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from utilities import load_env_from_yaml

app = Flask(__name__)

load_env_from_yaml('env.yaml')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'  # Example using SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

# Add more routes and logic for viewing data about an investment portfolio

if __name__ == '__main__':
    db.create_all()
    app.run()