from django.forms import ModelForm
from .models import Photo, Comment
from django import forms
from django.contrib.auth.models import User

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['comment', 'image']

class AppliForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['comment']

    def __init__(self, user, *args, **kwargs):
      super(AppliForm, self).__init__(*args, **kwargs)
    
class SearchForm(forms.Form):
    q = forms.CharField(label='キーワード')



class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
