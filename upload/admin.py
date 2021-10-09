from django.contrib import admin
from .forms import PickPhotoForm
from .models import PickPhoto


class ImageAdmin(admin.ModelAdmin):
    form = PickPhotoForm


admin.site.register(PickPhoto, ImageAdmin)