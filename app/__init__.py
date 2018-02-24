import os
from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES
import torch


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOADED_PHOTOS_DEST = 'uploads'

app = Flask(__name__, static_url_path="")
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = UPLOADED_PHOTOS_DEST
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

configure_uploads(app, photos)

# Load model
model = torch.load('models/resnet34')

from app import routes
