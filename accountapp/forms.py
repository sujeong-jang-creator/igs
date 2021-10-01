from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm

from .models import User


class UserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].disabled = True
        self.fields['email'].disabled = True

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password1', 'password2')

    email = forms.CharField(label='이메일')
    username = forms.CharField(label='이름', max_length=20)
    password = forms.CharField(label='현재 비밀번호', max_length=20, widget=forms.TextInput(
                attrs={'type': 'password', 'placeholder': 'your old Password', 'class': 'span'}))
    password1 = forms.CharField(label='새로운 비밀번호', max_length=20, widget=forms.TextInput(
        attrs={'type': 'password', 'placeholder': 'New Password', 'class': 'span'}))
    password2 = forms.CharField(label='현재 비밀번호 확인', max_length=20, widget=forms.TextInput(
        attrs={'type': 'password', 'placeholder': 'Confirm New Password', 'class': 'span'}))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

