from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from .models import Post, Tag
from .forms import PostForm
from django.urls import reverse_lazy
from .filters import PostFilter
from django.http import HttpResponse

class BlogPostView(DetailView):
    model = Post
    template_name = 'blog_post.html'

    def get_context_data(self, **kwargs):
        context = super(BlogPostView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all().order_by('-created_on')
        context['tag_list'] = Tag.objects.all()
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
        context['post_list'] = Post.objects.all().order_by('-created_on')
        context['tag_list'] = Tag.objects.all()
        return context

class TagsView(ListView):
    model = Tag
    template_name = 'tags.html'

    def filter_by_title(self):
        my_filter = PostFilter(self.request.GET, queryset=Post.objects.all())
        return my_filter

    def get_context_data(self, **kwargs):
        context = super(TagsView, self).get_context_data(**kwargs)
        context['post_list'] = self.filter_by_title().qs.order_by('-created_on')
        context['tag_list'] = Tag.objects.all().order_by('name')
        context['my_filter'] = self.filter_by_title()
        return context

class TagDetailView(DetailView):
    model = Tag
    template_name = 'tag_detail.html'

    def filter_by_title(self):
        my_filter = PostFilter(self.request.GET, queryset=Post.objects.all())
        return my_filter

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context['post_list'] = self.filter_by_title().qs.order_by('-created_on')
        context['tag_list'] = Tag.objects.all().order_by('name')
        context['my_filter'] = self.filter_by_title()
        return context