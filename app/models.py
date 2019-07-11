from django.db import models
from django.contrib.auth.models import User 

class Photo(models.Model):
    comment = models.TextField(max_length=1000)
    image = models.ImageField(upload_to = 'photos', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    share_id = models.IntegerField(default=-1)
    good_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.comment) + ' (' + str(self.user) + ')'
    
    def get_share(self):
        return Photo.objects.get(id=self.share_id)
    
    class Meta:
        ordering = ('-created_at',)
    
class Good(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    def __str__(self):
        return 'good for "' + str(self.photo) + '" (by ' + \
                str(self.user) + ')'
