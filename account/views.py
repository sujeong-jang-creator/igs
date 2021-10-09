from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.auth.forms import PasswordResetForm

from django.core.mail import EmailMessage

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from account.decorators import account_ownership_required
from account.forms import UserChangeForm, UserCreationForm
from account.models import HelloWorld, User

has_ownership = [account_ownership_required, login_required]


@login_required
def hello_world(request):

    if request.method == "POST":

        temp = request.POST.get('hello_world_input')

        new_hello_world = HelloWorld()
        new_hello_world.text = temp
        new_hello_world.save()

        hello_world_list = HelloWorld.objects.all()
        return HttpResponseRedirect(reverse('account:hello_world'))
    else:
        hello_world_list = HelloWorld.objects.all()
        return render(request, 'account/hello_world.html', context={'hello_world_list': hello_world_list})


class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('account:login')
    template_name = 'account/create.html'


@method_decorator(has_ownership, 'get')
class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('account:detail')
    template_name = 'account/detail.html'


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):
    model = User
    context_object_name = 'target_user'
    form_class = UserChangeForm
    template_name = 'account/update.html'

    def get_success_url(self):
        return reverse('account:detail', kwargs={'pk': self.object.pk})


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('account:login')
    template_name = 'account/delete.html'


def send_email(request):
    subject = "message"
    to = ["aaa@bbb.com"]
    from_email = "alphaca.igs@gmail.com"
    message = "test"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()


class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('account:login')
    template_name = 'account/create.html'


class UserPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    # success_url = reverse_lazy('password_reset_done')
    template_name = 'password_reset/password_reset.html'

    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'password_reset/password_reset_done_fail.html')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset/password_reset_confirm.html'
