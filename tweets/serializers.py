from rest_framework import serializers
from .models import Tweet, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class TweetSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    total_likes = serializers.ReadOnlyField()

    class Meta:
        model = Tweet
        fields = '__all__'

    def get_comments(self, obj):
        comments = obj.comments.all()
        return CommentSerializer(comments, many=True).data
