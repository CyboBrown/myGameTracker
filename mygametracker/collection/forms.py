from django import forms
from .models import Collection


class CollectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

    name = forms.CharField(label='', widget=forms.TextInput({
        'class': 'form-control mt-4',
        'placeholder': 'Collection Name'
    }))
    is_private = forms.BooleanField(label='Set as Private', required=False, widget=forms.CheckboxInput({
        'class': 'form-check-input',
        'style': 'float: left; margin-right: 10px; margin-top: 4px;'
    }))

    class Meta:
        model = Collection
        fields = ['name', 'is_private']
