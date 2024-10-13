from flask import Flask, render_template
from utilities import load_env_from_yaml

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Add more routes and logic for viewing data about an investment portfolio

if __name__ == '__main__':
    load_env_from_yaml('env.yaml')
    app.run()