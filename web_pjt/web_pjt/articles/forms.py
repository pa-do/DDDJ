from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
  class Meta:
    model = Article
    exclude = ['created_at', 'updated_at', 'user']
    labels = {'movie_title': '영화 제목', 'rank': '평점', 
    'title': '글 제목', 'content': '글 내용'}


class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['content']
    labels = {'content': '댓글'}