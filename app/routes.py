import requests
from PIL import Image
from io import BytesIO
import mimetypes
from urllib.request import urlopen, Request
from flask import render_template

from app import app
from .forms import ImageForm
from .detector import save_emotion_image


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    form = ImageForm()

    if form.validate_on_submit():

        # Get image and/or url data from form
        file = form.image.data
        url = form.url.data

        # Process whatever input was submitted
        if (file and allowed_file(file.filename)) or\
           (url and is_image_and_ready(url)):

            if file:
                bytes_image = file.read()
            else:
                bytes_image = requests.get(url).content

            img = Image.open(BytesIO(bytes_image))
            img_file = save_emotion_image(img)

            return render_template('index.html', image_file=img_file,
                                   scroll='predict', form=form)

    return render_template('index.html', form=ImageForm())


def allowed_file(filename):
    allowed_ext = app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext


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
