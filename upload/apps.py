from django.apps import AppConfig
from tensorflow.keras import models

class UploadConfig(AppConfig):
    name = 'upload'
    model = models.load_model("/engn/igs_venv/igs/model/YOLOv4") # AWS 에서의 경로, cuda 설치 후 경로 문제로 절대 경로로 수정
    # model = models.load_model(r".\model\YOLOv4")  
