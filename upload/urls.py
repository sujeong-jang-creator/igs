from django.urls import path
from upload.views import PickPhotoView
from . import views

app_name = "upload"

urlpatterns = [
    path('pick_photo/', PickPhotoView.as_view(), name='pick_photo'),
    path('predict', views.predict, name='predict'),
]
