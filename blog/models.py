from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from datetime import datetime, date
from django.urls import reverse
from account.models import User


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True, null=True, blank=True)
    special = models.CharField(max_length=1, default='#')
    description = models.TextField(max_length=512, default='Tag description.')
    updated_on = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['name']
  
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag-detail', kwargs={'slug': self.slug})


class Post(models.Model):
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    author_plug = models.URLField(max_length=128, default='https://linktr.ee/ndasilva')
    image = models.ImageField(null=True, blank=True, upload_to='blog_images/')
    image_alt_text = models.CharField(null=True, blank=True, max_length=255)
    tags = models.CharField(max_length=255, default='blog')
    summary = models.TextField(max_length=512)
    content = RichTextField(blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    #status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.updated_on.strftime("%Y-%m-%d")) + ' | ' + self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog-post', kwargs={'slug': self.slug})

    def get_tags(self):
        return self.tags.replace('[', '').replace(']', '').replace('\'', '').split(', ')
    
    def get_tags_and_slugs(self):
        names = self.tags.replace('[', '').replace(']', '').replace('\'', '').split(', ')
        slugs = (slugify(name) for name in names)
        return zip(names, slugs)
    
    def get_total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=512)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    
    class Meta:
        ordering = ['-created_on']
  
    def __str__(self):
        return str(self.user.pk) + ' | ' + str(self.user) + ' | ' + str(self.body) + ' | ' + str(self.post)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Dislike', 'Dislike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated_on = models.DateTimeField(auto_now= True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.pk) + ' | ' + str(self.user) + ' | ' + self.value + ' | ' + str(self.post)