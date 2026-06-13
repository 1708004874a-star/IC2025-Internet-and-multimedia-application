from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Category, Tag
from .forms import PostForm

try:
    import markdown
except ImportError:
    markdown = None


class PostListView(ListView):
    model = Post
    template_name = 'personal_blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = 'personal_blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        if markdown and post.content:
            context['rendered_content'] = markdown.markdown(
                post.content,
                extensions=['extra', 'codehilite', 'tables']
            )
        else:
            context['rendered_content'] = post.content

        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'personal_blog/post_form.html'
    success_url = reverse_lazy('personal_blog:post_list')


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'personal_blog/post_form.html'
    success_url = reverse_lazy('personal_blog:post_list')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'personal_blog/post_confirm_delete.html'
    success_url = reverse_lazy('personal_blog:post_list')


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, is_published=True)
    return render(request, 'personal_blog/post_list.html', {
        'posts': posts,
        'category': category
    })


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, is_published=True)
    return render(request, 'personal_blog/post_list.html', {
        'posts': posts,
        'tag': tag
    })
