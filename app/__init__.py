import os
from flask import Flask
from torch import load


app = Flask(__name__, static_url_path="")
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024


# Form
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or\
    'you-will-never-guess'

# Load model
model = load('models/resnet34')

from app import routes
