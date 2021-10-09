from django.forms import ModelForm

from upload.models import PickPhoto
from upload.widgets import FileInputWithPreview


class PickPhotoForm(ModelForm):
    class Meta:
        model = PickPhoto
        fields = ['image']
        # fields = '__all__'
        widgets = {
            'image': FileInputWithPreview()
        }
