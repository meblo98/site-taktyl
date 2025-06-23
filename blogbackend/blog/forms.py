from django import forms
from .models import Post, Comment
from ckeditor.widgets import CKEditorWidget



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'image')