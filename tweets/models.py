from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=250)
    image = models.ImageField(upload_to='tweet_images/', blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='tweets', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)  #twitter.com/my-1st-post

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:50])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name