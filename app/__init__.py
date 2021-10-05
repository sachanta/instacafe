from flask import Flask
from app import config
from flask_bootstrap import Bootstrap

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the views
from app import views

# Load the config file
app.config.from_object(config.Config)
Bootstrap(app)