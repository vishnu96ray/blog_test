from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.


BLOG_STATUS = ((1, 'DRAFT'), (2, 'PUBLISHED'))


class Blog(models.Model):
    title = models.CharField(null=False, max_length=50, blank=False)
    image = models.ImageField(upload_to="blog/", null=True, blank=True)
    description = models.TextField()
    status = models.IntegerField(choices=BLOG_STATUS, default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # author = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_allowed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(default=datetime.now)
    slug = models.SlugField(max_length=150, unique=True)

    
    
    def __str__(self):
        return self.title

@receiver(post_delete, sender=Blog)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_blog_post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify( instance.title)


pre_save.connect(pre_save_blog_post_reciever, sender=Blog)

# def __str__(self):
#         return self.title

# def get_tag_id(self):
#         return [str(i.id) for i in self.tag.all()]


# def save(self, *args, **kwargs):
#         if self.slug is None or self.slug == '' or self.status == 1:
#             self.slug = slugify(self.meta_title)
#         super(Blog, self).save(*args, **kwargs)