from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class AccountStaticSitemap(Sitemap):
	changefreq = "yearly"
	priority = 0.4
	
	def items(self):
		return ['account']
			
	def location(self, item):
		return reverse(item)


class RegistrationStaticSitemap(Sitemap):
	changefreq = "yearly"
	priority = 0.8
	
	def items(self):
		return ['login', 'sign_up', 'password_reset']
		
	def location(self, item):
		return reverse(item)