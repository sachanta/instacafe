from flask import Flask
from flask import render_template
from app import app
import logging

app = Flask(__name__)


logging.basicConfig(filename='demo.log', level=logging.DEBUG)

if __name__ == '__main__':
    app.run()