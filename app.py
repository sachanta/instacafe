# run.py

from app import app
import logging

logging.basicConfig(filename='demo.log', level=logging.DEBUG)

if __name__ == '__main__':
    app.run()
