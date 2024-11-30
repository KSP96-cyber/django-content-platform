from django import forms 
from .models import Blog


class BlogForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))  # HTML5 date picker)
    class Meta:
        model = Blog
        fields = ['title', 'description', 'date', 'location', 'image']
        
        
class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), required=True)
