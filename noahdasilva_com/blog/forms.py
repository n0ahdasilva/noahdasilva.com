from django import forms
from .models import Post, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'author_plug', 'image', 'tags', 'summary', 'content', 'status',]
        widgets = {
            'title' : forms.TextInput(attrs={'maxlength': 128, 'placeholder': 'Blog title'}),
            'author' : forms.Select(attrs={'placeholder': 'Blog author'}),
            'author_plug' : forms.URLInput(attrs={'placeholder': 'Author redirect plug (website, linktree, ...)'}),
            'image' : forms.FileInput(attrs={'placeholder': 'Blog image for preview and post page'}),
            'tags' : forms.SelectMultiple(choices='', attrs={'placeholder': 'Blog tags (separated by comma)'}),
            'summary' : forms.Textarea(attrs={'maxlength': 300, 'placeholder': 'Blog summary, max 255 characters (one or two sentences)...'}),
            'content' : forms.Textarea(attrs={'placeholder': 'Blog content, write away...'}),
            'status' : forms.Select(attrs={'placeholder': 'Is blog post a draft or ready to publish?'}),
        }
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['tags'] = forms.TypedMultipleChoiceField(choices=Tag.objects.all().values_list('name', 'name'))