from django.urls import path, include
from . import views
from .views import EditPostView, BlogPostView, AddPostView, EditPostView, DeletePostView

urlpatterns = [
    #path('', views.home, name="home"),
    path('blog/<slug:slug>', BlogPostView.as_view(), name="blog-post"),
    path('add-post/', AddPostView.as_view(), name="add-post"),
    path('blog/<slug:slug>/edit', EditPostView.as_view(), name="edit-post"),
    path('blog/<slug:slug>/remove', DeletePostView.as_view(), name="delete-post"),
]