from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Project


class ProjectSitemap(Sitemap):
		changefreq = "weekly"
		priority = 0.5
		
		def items(self):
				return Project.objects.all()

class PortfolioStaticSitemap(Sitemap):
		changefreq = "never"
		priority = 0.5
		
		def items(self):
				return ['portfolio',]
				
		def location(self, item):
				return reverse(item)