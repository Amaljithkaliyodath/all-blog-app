# # serializers.py
# from rest_framework import serializers
# from .models import BlogPost

# class BlogPostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BlogPost
#         fields = ['id', 'title', 'content', 'tags', 'created_at', 'updated_at', 'author']
#         read_only_fields = ['author', 'created_at', 'updated_at']
