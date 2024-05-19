from rest_framework import serializers
from .models import Category, Post, Comment, React

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','slug']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author','image_url', 'video_url', 'privacy_status', 'content', 'created_at', 'updated_at', 'category']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']

class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ['id', 'post', 'user', 'react_type', 'created_at']