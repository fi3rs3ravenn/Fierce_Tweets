from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tweets') 
    content = models.TextField(max_length=280)  
    media = models.FileField(upload_to='tweet_media/', blank=True, null=True) 
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_tweets', blank=True)
    retweet = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='retweets')
    slug = models.SlugField(unique=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.username}-{self.content[:50]}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

    @property
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments') 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} commented: {self.content[:30]}"
