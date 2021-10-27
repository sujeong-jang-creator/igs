from django.conf.urls import url
from django.urls import path

import upload
from upload import views
from . import views

app_name= "grading"

urlpatterns = [
    path('total_distinguish/', views.PostListView.as_view(), name='total_distinguish'),
    path('detail_distinguish/', views.PostListView2.as_view(), name='detail_distinguish'),
    path('show_detail/<int:result_pk>', views.show_detail, name='show_detail'),
]