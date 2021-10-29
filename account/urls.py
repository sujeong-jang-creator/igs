from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from account.views import AccountCreateView, AccountDetailView, AccountUpdateView, AccountDeleteView

app_name = "account"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('create/', AccountCreateView.as_view(), name='create'),
    path('detail/<int:pk>', AccountDetailView.as_view(), name='detail'),
    path('update/<int:pk>', AccountUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', AccountDeleteView.as_view(), name='delete'),
]
