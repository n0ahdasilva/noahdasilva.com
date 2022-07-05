from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy

class BlogPostView(DetailView):
    model = Post
    template_name = 'blog_post.html'

class AddPostView(CreateView):
    model = Post
    template_name = 'add_post.html'
    form_class = PostForm

class EditPostView(UpdateView):
    model = Post
    template_name = 'edit_post.html'
    form_class = PostForm

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')