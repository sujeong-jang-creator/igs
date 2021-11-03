from django.apps import AppConfig
from tensorflow.keras import models

class UploadConfig(AppConfig):
    name = 'upload'
    # model = models.load_model(r".\model\YOLOv4")
    model = None
