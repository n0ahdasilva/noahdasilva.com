import imp
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Post, Tag, Comment, Like
from .forms import PostForm, TagForm
from .filters import PostFilter
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class BlogPostView(DetailView):
    model = Post
    template_name = 'blog_post.html'

    def get_context_data(self, **kwargs):
        context = super(BlogPostView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()
        context['tag_list'] = Tag.objects.all()
        context['comment_list'] = Comment.objects.filter(post=self.object)
        context['total_comments'] = Comment.objects.filter(post=self.object).count()
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
    paginate_by = 6

    def filter_by_title(self):
        title_filter = PostFilter(self.request.GET, queryset=Post.objects.filter(tags__icontains=self.object))
        return title_filter

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['title_filter'] = self.filter_by_title()

        book_paginator = Paginator(self.filter_by_title().qs, self.paginate_by)
        page_num = self.request.GET.get('page')
        page = book_paginator.get_page(page_num)

        context['post_page'] = page
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
    model = Post
    template_name = 'tags.html'
    paginate_by = 6

    def filter_by_title(self):
        title_filter = PostFilter(self.request.GET, queryset=Post.objects.all())
        return title_filter
    
    def get_context_data(self, **kwargs):
        context = super(TagsView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['title_filter'] = self.filter_by_title()

        book_paginator = Paginator(self.filter_by_title().qs, self.paginate_by)
        page_num = self.request.GET.get('page')
        page = book_paginator.get_page(page_num)

        context['post_page'] = page
        return context


@login_required
def like_view(request, pk):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)
        
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

        post_obj.save()
        like.save()
            
    
    return HttpResponseRedirect(reverse('blog-post', kwargs={'slug': post_obj.slug}))


@login_required
def comment_view(request, pk):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        user_comment = request.POST.get('user_comment')
        post_obj = Post.objects.get(id=post_id)

        comment = Comment.objects.create(user=user, post=post_obj, body=user_comment)

        post_obj.save()
        comment.save()
            
    return HttpResponseRedirect(reverse('blog-post', kwargs={'slug': post_obj.slug}))


@login_required
def remove_comment_view(request, pk):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        Comment.objects.filter(id=pk).delete()
          
    return HttpResponseRedirect(reverse('blog-post', kwargs={'slug': post_obj.slug}))
