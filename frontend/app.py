from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Add more routes and logic for viewing data about an investment portfolio

if __name__ == '__main__':
    app.run()