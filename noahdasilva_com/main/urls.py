from django.urls import path, include
from . import views
from .views import HomeView, about_view, contact_view


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('about', views.about_view, name="about"),
    path('contact', views.contact_view, name="contact"),
]

handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'