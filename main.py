from flask import Flask, render_template
from data import db_session

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('news.html')


if __name__ == '__main__':
    app.run()