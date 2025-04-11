from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Item, Comment, BlogPost
from django.core.validators import MinValueValidator


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'quantity']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

class ItemForm(forms.ModelForm):
    quantity = forms.IntegerField(
        validators=[MinValueValidator(0)],
        initial=0,
        help_text="Initial stock quantity"
    )
    
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'quantity', 'is_featured']