from django.forms import ModelForm
from django import forms
from .models import User, UserFriend


class SignupForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    email = forms.EmailField(widget=forms.EmailInput({
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    birthdate = forms.DateField(widget=forms.DateInput({
        'type': 'date',
        'placeholder': 'yyyy-mm-dd (DOB)',
        'class': 'form-control'
    }))
    gender = forms.ChoiceField(choices=User.genders, widget=forms.Select({
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'birthdate', 'gender']


class LoginForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileUpdateForm(forms.Form):
    new_username = forms.CharField(widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'GayExpert420'
    }))
    new_password = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'placeholder': 'iLoveDeques69'
    }))
    new_email = forms.EmailField(widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'your_new_email@email.com...'
    }))
    new_bio = forms.CharField(widget=forms.Textarea({
        'class': 'form-control',
        'placeholder': 'Hello, I am...'
    }))
    new_gender = forms.ChoiceField(choices=[("M", "Male"), ("F", "Female")], widget=forms.Select(attrs={
        'class': 'form-control',
    }))
