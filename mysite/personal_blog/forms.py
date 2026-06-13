from django import forms
from .models import Post, Category, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 15,
                'class': 'form-control',
                'placeholder': 'Write your post content in Markdown...'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title...'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
