from django.contrib.auth.decorators import login_required
from django.shortcuts import render , get_object_or_404 , redirect
from .models import Tweet
from .forms import TweetForm , CommentForm
from django.db.models import Q

def tweet_list(request):
    if request.user.is_authenticated:
        tweets = Tweet.objects.filter(
            Q(user__in=request.user.following.all()) | Q(user=request.user)
        ).order_by('-created_at')
    else:
        tweets = Tweet.objects.all().order_by('-created_at')

    form = TweetForm()
    return render(request, 'tweets/tweet_list.html', {'tweets': tweets, 'form': form})

@login_required
def edit_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.user != tweet.user:
        return redirect('tweet_list')
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweets/edit_tweet.html' , {'form': form})

@login_required
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.user == tweet.user:
        tweet.delete()
    return redirect('tweet_list')

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)
    return redirect('tweet_list')

@login_required 
def add_comment(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.tweet = tweet 
            comment.save()
            return redirect('tweet_list')
    return redirect('tweet_list')

