from django.forms import ModelForm

from uploadapp.models import PickPhoto
from uploadapp.widgets import FileInputWithPreview


class PickPhotoForm(ModelForm):
    class Meta:
        model = PickPhoto
        fields = ['image']
        # fields = '__all__'
        widgets = {
            'image': FileInputWithPreview()
        }
