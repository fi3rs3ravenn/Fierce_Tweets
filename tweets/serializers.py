from rest_framework import serializers
from .models import Tweet, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class TweetSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True)
    total_likes = serializers.ReadOnlyField()

    class Meta:
        model = Tweet
        fields = '__all__'