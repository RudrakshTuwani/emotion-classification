import os
from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES


app = Flask(__name__, static_url_path="")
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
configure_uploads(app, photos)

from app import routes