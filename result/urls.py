from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = "result"

urlpatterns = [
    path('show_result/<int:result_pk>', views.show_result, name = "show_result"),
    path('revision/<int:result_pk>', views.revision, name = "revision"),
]
