# from django.forms import ModelForm
from django import forms
# from upload.models import PickPhoto
# from upload.widgets import FileInputWithPreview

class UploadForm(forms.Form):
    upimg = forms.ImageField()
    
# class PickPhotoForm(ModelForm):
#     class Meta:
#         model = PickPhoto
#         fields = ['image']
#         # fields = '__all__'
#         widgets = {
#             'image': FileInputWithPreview()
#         }