from django.urls import path, include
from . import views
from .views import EditPostView, BlogPostView, AddPostView, EditPostView, DeletePostView, BlogView, TagsView, TagDetailView

urlpatterns = [
    #path('', views.home, name="home"),
    path('blog/<slug:slug>', BlogPostView.as_view(), name="blog-post"),
    path('add-post/', AddPostView.as_view(), name="add-post"),
    path('blog/<slug:slug>/edit', EditPostView.as_view(), name="edit-post"),
    path('blog/<slug:slug>/remove', DeletePostView.as_view(), name="delete-post"),
    path('blog/', BlogView.as_view(), name="blog"),
    path('blog/tags/', TagsView.as_view(), name="tags"),
    path('blog/tags/<slug:slug>', TagDetailView.as_view(), name="tag-detail"),
]