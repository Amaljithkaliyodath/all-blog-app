from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True) # This will return the author's username

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'tags', 'created_at', 'updated_at', 'custom_id', 'author']
