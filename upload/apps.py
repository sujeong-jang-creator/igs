from django.apps import AppConfig
from tensorflow.keras import models

class UploadConfig(AppConfig):
    name = 'upload'
    model = models.load_model(r"\engn\igs_venv\igs\model\YOLOv4")
    # model = models.load_model(r".\model\YOLOv4")
