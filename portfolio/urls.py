from django.urls import path
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path('portfolio/<slug:slug>', views.ProjectView.as_view(), name="project"),
    path('add-project/', views.AddProjectView.as_view(), name="add-project"),
    path('portfolio/<slug:slug>/edit', views.EditProjectView.as_view(), name="edit-project"),
    path('portfolio/<slug:slug>/remove', views.DeleteProjectView.as_view(), name="delete-project"),
    path('portfolio/', views.PortfolioView.as_view(), name="portfolio"),
]