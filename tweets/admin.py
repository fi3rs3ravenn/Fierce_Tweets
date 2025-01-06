from django.contrib import admin
from .models import Tweet, Tag

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name' , 'created_at')
    