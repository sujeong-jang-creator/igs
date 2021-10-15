from django.db import models

class PickPhoto(models.Model):
    image = models.ImageField(upload_to='pick_photo/', null=False)
    comment = models.CharField(max_length=100, null=False)
