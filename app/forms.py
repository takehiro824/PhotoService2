from django.forms import ModelForm
from .models import Photo

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['comment', 'image']

class AppliForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['comment', 'image']

    def __init__(self, user, *args, **kwargs):
      super(AppliForm, self).__init__(*args, **kwargs)
      