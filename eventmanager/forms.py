from django import forms 
from .models import Advent
from django.utils import timezone

class AdventForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})  # HTML5 date picker
    )

    class Meta:
        model = Advent
        fields = ['title', 'description', 'date', 'location', 'adventmanager_image']



