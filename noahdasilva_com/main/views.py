from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from blog.models import Post
from django.urls import reverse_lazy

#def home(request):
#    return render(request, 'home.html', {})

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-created_on']

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'