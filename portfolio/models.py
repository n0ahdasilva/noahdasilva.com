from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Project(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True, null=True, blank=True)
    description = models.TextField(max_length=512)
    category = models.CharField(max_length=64)
    url = models.URLField(max_length=128, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='portfolio_images/')
    tags = models.CharField(max_length=128, default='website, HTML, CSS')
    updated_on = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('project', kwargs={'slug': self.slug})
    
    def get_tags(self):
        return self.tags.replace(', ', ',').split(',')