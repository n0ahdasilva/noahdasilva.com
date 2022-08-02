from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('about/',views.about_view, name="about"),
    path('terms-and-conditions/',views.terms_and_conditions_view, name="terms_and_conditions"),
    path('privacy-policy/',views.privacy_policy_view, name="privacy_policy"),
    path('contact/', views.ContactView.as_view(), name="contact"),
]

handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'