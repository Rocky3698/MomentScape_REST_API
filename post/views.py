from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Category, Post, Comment, React
from .serializers import CategorySerializer, PostSerializer, CommentSerializer, ReactSerializer
from django.db.models import Q
from rest_framework.authentication import  TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post_id')
        user_id = self.request.query_params.get('user_id')
        slug = self.request.query_params.get('slug')
        if post_id:
            queryset = queryset.filter(id=post_id)
        elif user_id:
            queryset = queryset.filter(author=user_id)
        elif slug:
            queryset = queryset.filter(~Q(privacy_status='only me'),category__slug=slug)
        else:
            queryset = queryset.filter(~Q(privacy_status='only me'))
        return queryset

class PublicPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(privacy_status='public')
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

class VideoPostsView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    def get_queryset(self):
        return Post.objects.exclude(video_url__isnull=True).exclude(video_url='')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post_id')
        comment_id = self.request.query_params.get('comment_id')
        if post_id:
            queryset = queryset.filter(post__id=post_id)
        if comment_id:
            queryset = queryset.filter(id=comment_id)
        return queryset


class ReactViewSet(viewsets.ModelViewSet):
    queryset = React.objects.all()
    serializer_class = ReactSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post__id=post_id)
        return queryset
    

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView

class PostReactionsSummary(APIView):
    def get(self, request, post_id,user_id):
        post = get_object_or_404(Post, id=post_id)
        total_likes = React.objects.filter(post=post, react_type='like').count()
        total_dislikes = React.objects.filter(post=post, react_type='dislike').count()
        liked = React.objects.filter(user__id=user_id, post=post, react_type='like').exists()
        disliked = React.objects.filter(user__id=user_id, post=post, react_type='dislike').exists()
        data = {
            'post_id': post_id,
            'total_likes': total_likes,
            'total_dislikes': total_dislikes,
            'liked':liked,
            'disliked':disliked
        }
        return JsonResponse(data)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class DeleteReactView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id, user_id):
        react = get_object_or_404(React, post_id=post_id, user_id=user_id)
        react.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateReactView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, post_id, user_id):
        react = get_object_or_404(React, post_id=post_id, user_id=user_id)
        serializer = ReactSerializer(react, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

