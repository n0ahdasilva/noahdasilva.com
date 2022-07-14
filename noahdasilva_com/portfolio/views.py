from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator


class ProjectView(DetailView):
    model = Project
    template_name = 'project.html'


@method_decorator([login_required, 
    permission_required("blog.add_project")], name='dispatch')
class AddProjectView(CreateView):
    model = Project
    template_name = 'add_project.html'
    form_class = ProjectForm


@method_decorator([login_required, 
    permission_required("blog.change_project")], name='dispatch')
class EditProjectView(UpdateView):
    model = Project
    template_name = 'edit_project.html'
    form_class = ProjectForm


@method_decorator([login_required, 
    permission_required("blog.delete_project")], name='dispatch')
class DeleteProjectView(DeleteView):
    model = Project
    template_name = 'delete_project.html'
    success_url = reverse_lazy('home')


class PortfolioView(ListView):
    model = Project
    template_name = 'portfolio.html'