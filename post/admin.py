from django.contrib import admin
from .models import Post, Comment , React, Category
# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(React)