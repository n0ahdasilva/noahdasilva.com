from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class HomeSitemap(Sitemap):
	changefreq = "weekly"
	priority = 1
	
	def items(self):
		return ['home']
			
	def location(self, item):
		return reverse(item)


class AboutSitemap(Sitemap):
	changefreq = "yearly"
	priority = 0.7
	
	def items(self):
		return ['about']
			
	def location(self, item):
		return reverse(item)


class ContactSitemap(Sitemap):
	changefreq = "yearly"
	priority = 0.8
	
	def items(self):
		return ['contact']
			
	def location(self, item):
		return reverse(item)


class LegalSitemap(Sitemap):
	changefreq = "yearly"
	priority = 0.4
	
	def items(self):
		return ['terms_and_conditions', 'privacy_policy',]
			
	def location(self, item):
		return reverse(item)