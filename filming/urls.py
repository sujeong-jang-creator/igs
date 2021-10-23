from django.urls import path
from . import views

app_name = "filming"

urlpatterns = [
    path('', views.take_photo, name='index'),
    # path('show_result/<int:pk>', views.show_result, name = "show_result"),
]
