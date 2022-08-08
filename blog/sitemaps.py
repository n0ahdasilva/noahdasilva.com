from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Tag
from .models import Post


class TagSitemap(Sitemap):
		changefreq = "weekly"
		priority = 0.5
		
		def items(self):
				return Tag.objects.all()


class PostSitemap(Sitemap):
		changefreq = "weekly"
		priority = 0.5
		
		def items(self):
				return Post.objects.all()
		
		def lastmod(self, obj):
				return obj.updated_on

class BlogStaticSitemap(Sitemap):
		changefreq = "never"
		priority = 0.5
		
		def items(self):
				return ['blog', 'tags']
				
		def location(self, item):
				return reverse(item)