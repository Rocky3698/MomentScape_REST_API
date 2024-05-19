from django.db import models
from .constants import ACCESS_TYPE, REACT_TYPES
from user.models import UserAccount
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name= models.CharField(max_length=20)
    slug = models.SlugField(unique=True,null=True,blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}")
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.name

class Post(models.Model):
    content = models.TextField()
    image_url = models.CharField(max_length=150, null = True, blank= True)
    video_url = models.CharField(max_length=150, null= True, blank=True)
    privacy_status = models.CharField(max_length=10,choices=ACCESS_TYPE, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserAccount,on_delete= models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    def __str__(self) -> str:
        return f'{self.author.username} post'

class React(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='reactions')
    react_type = models.CharField(max_length=10, choices=REACT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('post', 'user')
    def __str__(self):
        return f'{self.react_type} by {self.user} on {self.post}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.author.username} post'
