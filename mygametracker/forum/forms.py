from django import forms
from .models import Forum, Post


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'description']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']