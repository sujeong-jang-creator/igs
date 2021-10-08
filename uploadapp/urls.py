from django.urls import path

from uploadapp.views import PickPhotoView

app_name = "uploadapp"

urlpatterns = [
    path('pick_photo/', PickPhotoView.as_view(), name='pick_photo'),
]


