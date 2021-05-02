from django.db import models
from django.contrib.auth.models import User
import uuid
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class BaseModel(models.Model):
    # Base model for all models to extend
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True  # abstract class


class Post(BaseModel):  # post models
    user = models.ForeignKey(User, verbose_name="Posted by",
                             on_delete=models.CASCADE, related_name="photo_posts")
    photo = ProcessedImageField(upload_to="photos", format="JPEG", options={
                                "quality": 100}, processors=[ResizeToFit(width=1200, height=1200)])
    title = models.CharField(max_length=100, verbose_name='Post Title')
    content = models.TextField()
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Date of posted')
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post: {self.title} posted by {self.user} at {self.created_date}"

    class Meta:
        ordering = ["-created_date"]


class Like(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_likes")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_likes")
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Date of liked")

    def __str__(self):
        return f"{self.user} like"

    class Meta:
        unique_together = (("user", "post"))
        ordering = ["-created_date"]


class Comment(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_comments")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments")
    content = models.TextField(max_length=2000)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Date of commented")

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-created_date"]
