from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from upload.forms import PickPhotoForm
from upload.models import PickPhoto


class PickPhotoView(CreateView):
    model = PickPhoto
    context_object_name = 'pick_photo'
    form_class = PickPhotoForm
    success_url = reverse_lazy('account:hello_world')
    template_name = 'upload/pick_photo.html'

    # def form_valid(self, form):
    #     temp_pick_photo = form.save(commit=False)
    #     temp_pick_photo.user = self.request.user
    #     temp_pick_photo.save()
    #
    #     return super().form_valid(form)