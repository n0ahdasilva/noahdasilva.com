from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class MainStaticSitemap(Sitemap):
		changefreq = "never"
		priority = 0.5
		
		def items(self):
				return ['home', 'about', 'terms_and_conditions', 'privacy_policy', 'contact']
				
		def location(self, item):
				return reverse(item)