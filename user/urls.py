from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'author', views.Author, basename='author')

router = DefaultRouter()
router.register(r'author', views.Author, basename='author')
urlpatterns = [
    path('register/',views.UserRegisterView.as_view(),name='register'),
    path('login/',views.UserLoginApiView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
    path('',views.UserView.as_view(),name='user'),
    path('', include(router.urls)),
]