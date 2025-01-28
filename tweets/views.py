from django.contrib.auth.decorators import login_required
from django.shortcuts import render , get_object_or_404 , redirect
from .models import Tweet
from .forms import TweetForm , CommentForm
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TweetSerializer



def all_tweets(request):
    tweets = Tweet.objects.all().order_by('-cretaed_at')
    form = TweetForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = TweetForm(request.POST , request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweets:all_tweets')
    return render(request, 'tweets/tweet_list.html' , {'tweets':tweets , 'form':form})

def sub_tweets(request):
    tweets = Tweet.objects.filter(
        Q(user__in=request.user.following.all())
    ).order_by('-created_at')
    return render(request, 'tweets/tweet_list.html', {'tweets':tweets})



@login_required
def tweet_detail(request, slug):
    tweet = get_object_or_404(Tweet, slug=slug)
    comments = tweet.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.tweet = tweet 
            comment.save()
            return redirect('tweets:tweet_detail', slug=slug)
    else:
        form = CommentForm()

    return render(
        request, 'tweets/tweet_detail.html', {
            'tweet': tweet,
            'comments': comments,
            'form':form,
        }
    )


@login_required
def edit_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.user != tweet.user:
        return redirect('tweets:tweet_list')
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweets:tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweets/edit_tweet.html' , {'form': form})

@login_required
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.user == tweet.user:
        tweet.delete()
    return redirect('tweets:tweet_list')

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)
    return redirect('tweets:tweet_list')

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
            return redirect('tweets:tweet_list')
    return redirect('tweets:tweet_list')


class TweetListCreateAPIView(APIView):
    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets , many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
