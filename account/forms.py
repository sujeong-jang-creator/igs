from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    email = forms.CharField(label='이메일', max_length=100, widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': 'email', 'class': 'span'}))
    username = forms.CharField(label='이름', max_length=20, widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': 'username', 'class': 'span'}))
    password1 = forms.CharField(label='비밀번호', max_length=20, widget=forms.PasswordInput(
        attrs={'type': 'password', 'placeholder': 'password', 'class': 'span'}))
    password2 = forms.CharField(label='비밀번호 확인', max_length=20, widget=forms.PasswordInput(
        attrs={'type': 'password', 'placeholder': 'confirm password', 'class': 'span'}))


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


class UserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].disabled = True
        self.fields['email'].disabled = True

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password1', 'password2')

    email = forms.CharField(label='이메일', max_length=100)
    username = forms.CharField(label='이름', max_length=20)
    password = forms.CharField(label='현재 비밀번호', max_length=20, widget=forms.PasswordInput(
                attrs={'type': 'password', 'placeholder': 'your old Password', 'class': 'span'}))
    password1 = forms.CharField(label='새로운 비밀번호', max_length=20, widget=forms.PasswordInput(
        attrs={'type': 'password', 'placeholder': 'New Password', 'class': 'span'}))
    password2 = forms.CharField(label='새로운 비밀번호 확인', max_length=20, widget=forms.PasswordInput(
        attrs={'type': 'password', 'placeholder': 'Confirm New Password', 'class': 'span'}))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(("새로운 비밀번호가 서로 일치하지 않습니다."))
            if self.cleaned_data['password'] == self.cleaned_data['password1']:
                raise forms.ValidationError(("새로운 비밀번호가 이전과 동일합니다."))
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
