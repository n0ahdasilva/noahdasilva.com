from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Tag
from .models import Post


class TagSitemap(Sitemap):
	changefreq = "yearly"
	priority = 0.6
	
	def items(self):
		return Tag.objects.all()
	
	def lastmod(self, obj):
		return obj.date_updated


class PostSitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.7
	
	def items(self):
		return Post.objects.all()
	
	def lastmod(self, obj):
		return obj.updated_on
			

class BlogStaticSitemap(Sitemap):
	changefreq = "weekly"
	priority = 0.9
	
	def items(self):
		return ['blog', 'tags']
			
	def location(self, item):
		return reverse(item)

	def lastmod(self):
		return '2022-08-08'