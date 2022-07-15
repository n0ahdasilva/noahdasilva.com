from django.urls import path, include
from . import views


urlpatterns = [
    #path('', views.home, name="home"),
    path('blog/', views.BlogView.as_view(), name="blog"),
    path('blog/<slug:slug>', views.BlogPostView.as_view(), name="blog-post"),
    path('add-post/', views.AddPostView.as_view(), name="add-post"),
    path('blog/<slug:slug>/edit', views.EditPostView.as_view(), name="edit-post"),
    path('blog/<slug:slug>/remove', views.DeletePostView.as_view(), name="delete-post"),
    path('tags/', views.TagsView.as_view(), name="tags"),
    path('tags/<slug:slug>', views.TagDetailView.as_view(), name="tag-detail"),
    path('add-tag/', views.AddTagView.as_view(), name="add-tag"),
    path('tags/<slug:slug>/edit', views.EditTagView.as_view(), name="edit-tag"),
    path('tags/<slug:slug>/remove', views.DeleteTagView.as_view(), name="delete-tag"),
    path('like/<int:pk>', views.like_view, name="like_post"),
]