from io import BytesIO

import requests
from PIL import Image
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import Optional, URL

ER_MESSAGE_NOT_IMAGE = (
    'Пожалуйста, выберите изображение или введите URL-адрес'
)
ER_MESSAGE_URL_CODE_NOT_200 = (
    'Не удалось загрузить изображение по данному URL-адресу'
)
ER_MESSAGE_URL_CONNECTION_FILED = (
    'Ошибка при установлении соединения, проверьте пожалуйста ссылку'
)
ER_MESSAGE_INVALID_FORMAT = 'Неверный формат изображения'


class ImageUploadForm(FlaskForm):
    image = FileField(label='Выберите изображние')
    image_url = StringField(
        label='или прикрепите ссылку на изображение',
        validators=[
            URL(True, message='Пожалуйста, введите корректный URL-адрес'),
            Optional()
        ]
    )
    submit = SubmitField(label="Загрузить картинку")
    error_message = None

    def validate(self, extra_validators=None):
        if not self.image.data and not self.image_url.data:
            self.error_message = ER_MESSAGE_NOT_IMAGE
            return False
        if not super().validate(extra_validators):
            return False
        if self.image_url.data:
            try:
                response = requests.get(self.image_url.data)
                if response.status_code != 200:
                    self.image_url.errors.append(ER_MESSAGE_URL_CODE_NOT_200)
                    return False
            except requests.exceptions.RequestException:
                self.image_url.errors.append(ER_MESSAGE_URL_CONNECTION_FILED)
                return False
            if not self.verify_image(BytesIO(response.content)):
                self.image_url.errors.append(ER_MESSAGE_INVALID_FORMAT)
                return False
        if self.image.data:
            if not self.verify_image(self.image.data.stream):
                self.image.errors.append(ER_MESSAGE_INVALID_FORMAT)
                return False

        return True

    @staticmethod
    def verify_image(stream):
        try:
            Image.open(stream).verify()
            return True
        except (IOError, OSError):
            return False
