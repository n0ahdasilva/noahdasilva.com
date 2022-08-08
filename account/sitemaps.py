from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class AccountStaticSitemap(Sitemap):
		changefreq = "never"
		priority = 0.5
		
		def items(self):
				return ['login', 'sign_up', 'dashboard', 'password_reset']
				
		def location(self, item):
				return reverse(item)