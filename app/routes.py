import os
import requests
from PIL import Image
from io import StringIO, BytesIO
import mimetypes
from urllib.request import urlopen, Request
import numpy as np
import cv2
import uuid
from app import app
from flask import render_template, request, redirect, url_for
from .detector import detect_faces, draw_rects


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


def is_url_image(url):
    mimetype, encoding = mimetypes.guess_type(url)
    return (mimetype and mimetype.startswith('image'))


def check_url(url):
    """Returns True if the url returns a response code between 200-300,
       otherwise return False.
    """
    try:
        headers = {
            "Range": "bytes=0-10",
            "User-Agent": "MyTestAgent",
            "Accept": "*/*"
        }

        req = Request(url, headers=headers)
        response = urlopen(req)
        return response.code in range(200, 209)

    except Exception as e:
        return False


def is_image_and_ready(url):
    return is_url_image(url) and check_url(url)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    """if request.get_data('image_url'):
        url = request.get_data('image_url')
        # Check if url is a valid image url
        if is_image_and_ready(url):
            r = requests.get(url)
            img = Image.open(StringIO(r.content))
            return 'Image Found!'
        else:
            return redirect(url_for('index'))"""

    for f in os.listdir('app/static/temp/'):
        os.remove('app/static/temp/' + f)

    if 'image' in request.files:
        file = request.files['image']
        im = Image.open(BytesIO(file.read()))
        image = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        pil_image = draw_rects(image, detect_faces(image))
        image_file = 'temp/' + uuid.uuid4().hex + '.jpg'
        pil_image.save('app/static/' + image_file)

        return render_template('index.html', image_file=image_file,
                               scroll='predict')

    else:
        return redirect(url_for('index'))
