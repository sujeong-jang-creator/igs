from django.conf.urls import url
from django.urls import path
from . import views

app_name= "grading"

urlpatterns = [
    path('total_distinguish/', views.total_distinguish, name='total_distinguish'),
    path('detail_distinguish/', views.detail_distinguish, name='detail_distinguish'),
]