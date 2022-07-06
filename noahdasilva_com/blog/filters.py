import django_filters
from django_filters import DateFilter, CharFilter
from .models import Post, Tag


class PostFilter(django_filters.FilterSet):
    
    title = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = 'title', 'tags'
        exclude = ['tags']
