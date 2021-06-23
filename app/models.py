from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, Transpose
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    # Base model for all models to extend
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True  # abstract class


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Post(BaseModel):  # post models
    user = models.ForeignKey(User, verbose_name="Posted by",
                             on_delete=models.CASCADE, related_name="user_posts")
    photo = ProcessedImageField(upload_to="photos", format="JPEG", options={
                                "quality": 100}, processors=[Transpose(), ResizeToFit(width=1200, height=1200)])
    title = models.CharField(max_length=100, verbose_name='Post Title')
    content = models.TextField()
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Date of posted')
    updated_date = models.DateTimeField(auto_now=True)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    tags = TaggableManager(through=UUIDTaggedItem)

    def __str__(self):
        return f"Post: {self.title} posted by {self.user} at {self.created_date}"

    class Meta:
        ordering = ["-created_date"]


class Like(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_likes")
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
        User, on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments")
    content = models.TextField(max_length=2000)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Date of commented")

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-created_date"]


class Profile(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_profile")
    avatar = ProcessedImageField(upload_to="avatars", format="JPEG", options={
                                 "quality": 100}, processors=[Transpose(), ResizeToFit(width=500, height=500)], default="defaults/person.png")
    bio = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} 's Profile"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


class UserFollowing(BaseModel):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"
