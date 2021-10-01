# from django.contrib.auth.models import User

from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

from accountapp.models import User


def account_ownership_required(func):
    def decorated(request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        if not user == request.user:
            # return HttpResponseForbidden()
            return HttpResponseRedirect(reverse('accountapp:login'))
        return func(request, *args, **kwargs)

    return decorated