from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from .slugHelpers import *
from ckeditor.fields import RichTextField


# Create your models here.

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = RichTextField(blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)
    content = RichTextField(blank=True, null=True)

    # def __str__(self):
    #     return self.title + " by " + self.user

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(Post, self).save(*args, **kwargs)


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
