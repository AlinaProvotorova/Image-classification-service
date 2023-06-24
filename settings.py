import os
from torchvision.models import convnext_large, ConvNeXt_Large_Weights


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', '123qwe')
    FLASK_ENV = os.getenv("FLASK_ENV")


WEIGHTS = ConvNeXt_Large_Weights.DEFAULT
MODEL = convnext_large(weights=WEIGHTS)
