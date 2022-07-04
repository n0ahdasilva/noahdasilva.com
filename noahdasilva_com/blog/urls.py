from django.urls import path, include
#from . import views
from .views import HomeView, BlogPostView

urlpatterns = [
    #path('', views.home, name="home"),
    path('', HomeView.as_view(), name="home"),
    path('blog/<int:pk>', BlogPostView.as_view(), name="blog-post"),
]