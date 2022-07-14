from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Project
from .forms import ProjectForm


class ProjectView(DetailView):
    model = Project
    template_name = 'project.html'


class AddProjectView(CreateView):
    model = Project
    template_name = 'add_project.html'
    form_class = ProjectForm


class EditProjectView(UpdateView):
    model = Project
    template_name = 'edit_project.html'
    form_class = ProjectForm


class DeleteProjectView(DeleteView):
    model = Project
    template_name = 'delete_project.html'
    success_url = reverse_lazy('home')


class PortfolioView(ListView):
    model = Project
    template_name = 'portfolio.html'