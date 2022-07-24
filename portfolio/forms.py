from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'slug', 'description', 'category', 'url', 'image', 'tags',]
        widgets = {
            'name' : forms.TextInput(attrs={'maxlength': 128, 'placeholder': 'Project name'}),
            'description' : forms.Textarea(attrs={'maxlength': 512, 'placeholder': 'Project summary, max 512 characters...'}),
            'category' : forms.TextInput(attrs={'maxlength': 64, 'placeholder': 'Project category (website, app, etc.)'}),
            'url' : forms.URLInput(attrs={'maxlength': 128, 'placeholder': 'Project redirect (website, client social page, ...)'}),
            'image' : forms.FileInput(attrs={'placeholder': 'Image to showcase work in preview and project page...'}),
            'tags' : forms.TextInput(attrs={'maxlength': 128, 'placeholder': 'Project tags (seperate by comma)...'}),
        }