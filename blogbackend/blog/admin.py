from django.contrib import admin
from .models import Post, Comment, Category

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'category')
    list_filter = ('published_date', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInline]

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)