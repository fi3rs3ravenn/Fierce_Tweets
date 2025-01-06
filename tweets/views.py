from django.shortcuts import render , get_object_or_404
from .models import Tweet

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweets/tweet_list.html' , {'tweets':tweets})

def tweet_detail(request, slug):
    tweet = get_object_or_404(Tweet, slug=slug)
    return render(request, 'tweets/tweet_detail.html', {'tweet':tweet})

