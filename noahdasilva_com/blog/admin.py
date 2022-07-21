from django.contrib import admin
from .models import Post, Tag, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_on', 'updated_on',]
    list_filter = ['author',]
    readonly_fields = ['slug', 'updated_on', 'created_on']

admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Like)