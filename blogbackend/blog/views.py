from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from django.views.generic import TemplateView


def post_list(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    
    if category_id:
        posts = Post.objects.filter(category__id=category_id)
    else:
        posts = Post.objects.all()
    
    paginator = Paginator(posts, 5)  # 5 posts par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved_comment=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post_list')


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    
class FrontendAppView(TemplateView):
    template_name = 'base.html'