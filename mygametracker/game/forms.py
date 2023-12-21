from django.forms import ModelForm, DateInput
from django import forms
from .models import Game


class AddNewGameForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Title'
    }))

    genre = forms.CharField(widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Genre'
    }))

    description = forms.CharField(widget=forms.Textarea({
        'class': 'form-control',
        'placeholder': 'Description'
    }))

    release_date = forms.DateField(widget=DateInput({
        'type': 'date',
        'class': 'form-control'
    }))

    image = forms.CharField(widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Image (Optional)'
    }), required=False)

    class Meta:
        model = Game
        fields = ['title', 'genre', 'description', 'release_date', 'image']