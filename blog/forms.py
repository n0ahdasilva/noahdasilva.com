from django import forms
from .models import Post, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'author_plug', 'image', 'image_alt_text', 'tags', 'summary', 'content',]
        widgets = {
            'title' : forms.TextInput(attrs={'maxlength': 128, 'placeholder': 'Blog title'}),
            'author' : forms.Select(attrs={'placeholder': 'Blog author'}),
            'author_plug' : forms.URLInput(attrs={'maxlength': 128, 'placeholder': 'Author redirect plug (website, linktree, ...)'}),
            'image' : forms.FileInput(attrs={'placeholder': 'Blog image for preview and post page'}),
            'image_alt_text' : forms.TextInput(attrs={'maxlength': 255, 'placeholder': 'Alt text for image'}),
            'tags' : forms.SelectMultiple(choices='', attrs={'placeholder': 'Blog tags (separated by comma)'}),
            'summary' : forms.Textarea(attrs={'maxlength': 512, 'placeholder': 'Blog summary, max 512 characters (one or two sentences)...'}),
            'content' : forms.Textarea(attrs={'placeholder': 'Blog content, write away...'}),
        }
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['tags'] = forms.TypedMultipleChoiceField(choices=Tag.objects.all().values_list('name', 'name'))


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'special', 'description',]
        widgets = {
            'name' : forms.TextInput(attrs={'maxlength': 64, 'placeholder': 'Tag name...'}),
            'special' : forms.TextInput(attrs={'maxlength': 1, 'placeholder': 'Special character/icon...'}),
            'description' : forms.Textarea(attrs={'maxlength': 512, 'placeholder': 'Tag description...'}),
        }
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(TagForm, self).__init__(*args, **kwargs)
