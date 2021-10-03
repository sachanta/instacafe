from flask import Flask
from flask import render_template
from app import app

app = Flask(__name__)



if __name__ == '__main__':
    app.run()