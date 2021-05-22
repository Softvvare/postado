from django.contrib import admin
from app.models import Post, Like, Comment
# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
