from django.conf.urls import url
from django.urls import path
from . import views

app_name= "grading"

urlpatterns = [
    path('total_distinguish/', views.PostListView.as_view(), name='total_distinguish'),
    path('detail_distinguish/', views.PostListView2.as_view(), name='detail_distinguish'),
]