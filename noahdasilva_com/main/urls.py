from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('about',views.about_view, name="about"),
    path('contact', views.contact_view, name="contact"),
]

handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'