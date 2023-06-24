from io import BytesIO

import requests
from PIL import Image
from flask import render_template

from . import app
from .forms import ImageUploadForm
from .servise_classify_image import classify_image
from .servise_translate import translate_text


@app.route('/', methods=['GET', 'POST'])
def upload_image_view():
    form = ImageUploadForm()
    if form.validate_on_submit():
        file = form.image.data
        if file:
            image = Image.open(file.stream)
        else:
            image_url = form.image_url.data
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))

        image_width, image_height = image.size
        predicted_label = classify_image(image)
        return render_template('index.html',
                               form=form,
                               image_width=image_width,
                               image_height=image_height,
                               predicted_label=translate_text(predicted_label)
                               )
    return render_template('index.html', form=form)
