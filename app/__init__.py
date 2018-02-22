import os
from flask import Flask


app = Flask(__name__, static_url_path="")

# Configure options for uploading images
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes