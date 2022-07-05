from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from .models import Post, Tag
from .forms import PostForm
from django.urls import reverse_lazy

class BlogPostView(DetailView):
    model = Post
    template_name = 'blog_post.html'

    def get_context_data(self, **kwargs):
        context = super(BlogPostView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all().order_by('-created_on')
        return context

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

class BlogView(ListView):
    model = Post
    template_name = 'blog.html'
    
    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()
        context['tag_list'] = Tag.objects.all()
        return context

class TagsView(ListView):
    model = Post
    template_name = 'tags.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(TagsView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all().order_by('-created_on')
        context['tag_list'] = Tag.objects.all().order_by('name')
        return context