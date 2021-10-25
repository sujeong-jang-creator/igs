from django.urls import path
# from upload.views import PickPhotoView
from . import views
from django.views.generic import TemplateView

app_name = "upload"

urlpatterns = [
    # path('pick_photo/', PickPhotoView.as_view(), name='pick_photo'),
    path('pick_photo', TemplateView.as_view(template_name='upload/pick_photo.html'), name='pick_photo'),
    path('predict', views.predict, name='predict'),
]
