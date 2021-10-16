from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = "result"

urlpatterns = [
    path('result/<int:pk>', views.result, name = "result"),
    path('revision/<int:pk>', views.revision, name = "revision"),
]
