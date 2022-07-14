from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Tag
from .forms import PostForm, TagForm
from .filters import PostFilter
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator


class BlogPostView(DetailView):
    model = Post
    template_name = 'blog_post.html'

    def get_context_data(self, **kwargs):
        context = super(BlogPostView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()
        context['tag_list'] = Tag.objects.all()
        return context


@method_decorator([login_required, 
    permission_required("blog.add_post")], name='dispatch')
class AddPostView(CreateView):
    model = Post
    template_name = 'add_post.html'
    form_class = PostForm


@method_decorator([login_required, 
    permission_required("blog.change_post")], name='dispatch')
class EditPostView(UpdateView):
    model = Post
    template_name = 'edit_post.html'
    form_class = PostForm


@method_decorator([login_required, 
    permission_required("blog.delete_post")], name='dispatch')
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


class TagDetailView(DetailView):
    model = Tag
    template_name = 'tag_detail.html'

    def filter_by_title(self):
        title_filter = PostFilter(self.request.GET, queryset=Post.objects.filter(tags__icontains=self.object))
        return title_filter

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context['post_list'] = self.filter_by_title().qs
        context['title_filter'] = self.filter_by_title()
        return context


@method_decorator([login_required, 
    permission_required("blog.add_tag")], name='dispatch')
class AddTagView(CreateView):
    model = Tag
    template_name = 'add_tag.html'
    form_class = TagForm


@method_decorator([login_required, 
    permission_required("blog.change_tag")], name='dispatch')
class EditTagView(UpdateView):
    model = Tag
    template_name = 'edit_tag.html'
    form_class = TagForm


@method_decorator([login_required, 
    permission_required("blog.delete_tag")], name='dispatch')
class DeleteTagView(DeleteView):
    model = Tag
    template_name = 'delete_tag.html'
    success_url = reverse_lazy('home')


class TagsView(ListView):
    model = Tag
    template_name = 'tags.html'

    def filter_by_title(self):
        title_filter = PostFilter(self.request.GET, queryset=Post.objects.all())
        return title_filter

    def get_context_data(self, **kwargs):
        context = super(TagsView, self).get_context_data(**kwargs)
        context['post_list'] = self.filter_by_title().qs
        context['tag_list'] = Tag.objects.all()
        context['title_filter'] = self.filter_by_title()
        return context