from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register(r'posts', views.PostViewSet, basename='post')
router.register('public', views.PublicPostViewSet, basename='publicpost')
router.register('comment', views.CommentViewSet, basename='comment')
router.register('react', views.ReactViewSet, basename='react')
router.register('category', views.CategoryViewSet, basename='category')
router.register('videos',views.VideoPostsView,basename='videos')
urlpatterns = [
    path('', include(router.urls)),
    path('<int:post_id>/reactions/summary/<int:user_id>', views.PostReactionsSummary.as_view(), name='post-reactions-summary'),
    path('react/delete/<int:post_id>/<int:user_id>/', views.DeleteReactView.as_view(), name='delete-react'),
    path('react/update/<int:post_id>/<int:user_id>/', views.UpdateReactView.as_view(), name='update-react'),
]
