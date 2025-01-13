from django.contrib.auth.decorators import login_required
from django.shortcuts import render , get_object_or_404 , redirect
from .models import Tweet
from .forms import TweetForm

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweets/tweet_list.html' , {'tweets':tweets})

def tweet_detail(request, slug):
    tweet = get_object_or_404(Tweet, slug=slug)
    return render(request, 'tweets/tweet_detail.html', {'tweet':tweet})

@login_required
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            form.save_m2m() 
            return redirect('home')
    else:
        form = TweetForm()
    return render(request, 'tweets/create_tweet.html', {'form': form})
