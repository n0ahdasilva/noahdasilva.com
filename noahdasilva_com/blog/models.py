from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from datetime import datetime, date
from django.urls import reverse


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_plug = models.URLField(max_length=255, default='https://linktr.ee/ndasilva')
    image = models.ImageField(null=True, blank=True, upload_to='blog_images/')
    tags = models.CharField(max_length=255, default='blog')
    summary = models.TextField(max_length=300)
    content = RichTextField(blank=True, null=True)
    updated_on = models.DateTimeField(auto_now= True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return str(self.updated_on) + ' | ' + self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog-post', kwargs={'slug': self.slug})

    def get_tags(self):
        return self.tags.replace('[', '').replace(']', '').replace('\'', '').split(',')


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})