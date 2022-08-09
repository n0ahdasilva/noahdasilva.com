from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Project


class ProjectSitemap(Sitemap):
	changefreq = "yearly"
	priority = 0.7
	
	def items(self):
		return Project.objects.all()
	
	def lastmod(self, obj):
		return obj.updated_on
			

class PortfolioStaticSitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.8
	
	def items(self):
		return ['portfolio',]
			
	def location(self, item):
		return reverse(item)