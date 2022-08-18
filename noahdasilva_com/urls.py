"""noahdasilva_com URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from account.sitemaps import AccountStaticSitemap, RegistrationStaticSitemap
from blog.sitemaps import TagSitemap, PostSitemap, BlogStaticSitemap
from main.sitemaps import HomeSitemap, AboutSitemap, ContactSitemap, LegalSitemap
from portfolio.sitemaps import ProjectSitemap, PortfolioStaticSitemap


sitemaps = {
    'home': HomeSitemap,
    'about': AboutSitemap,
    'contact': ContactSitemap,
    'legal': LegalSitemap,
    'account': AccountStaticSitemap,
    'registration-static': RegistrationStaticSitemap,
    'blog-static': BlogStaticSitemap,
    'portfolio-static': PortfolioStaticSitemap,
    'tags': TagSitemap,
    'posts': PostSitemap,
    'projects': ProjectSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('blog.urls')),
    path('', include('account.urls')),
#    path('', include('django.contrib.auth.urls')),
    path('', include('portfolio.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
	    name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt",TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
 + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
