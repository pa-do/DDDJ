from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from movies.models import Movie
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import timedelta
import datetime
from django.utils import timezone


def index(request):
  articles = Article.objects.order_by('-pk')
  check_now = timezone.now()      # 현재 시간 기준으로 6시간 이내에 작성한 글에는 new를 띄우기 위한 timedelta값
  check_delta = timezone.now() - timedelta(hours=6)   # 이 값을 index.html로 넘겨 html단에서 처리한다.

  paginator = Paginator(articles, 15) # 숫자만 변경하면 한 페이지에 들어갈 글 수를 변경할 수 있음
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    'articles': articles,
    'page_obj': page_obj,
    'check_delta' : check_delta,
    'check_now' : check_now,
  }
  return render(request, 'articles/index.html', context)



@login_required
def create(request):
  if request.method == 'POST':
    form = ArticleForm(request.POST)
    if form.is_valid():
      article = form.save(commit=False)
      article.user = request.user
      article.save()
      return redirect('articles:detail', article.pk)
  else:
    form = ArticleForm()
  context = {
    'form': form,
  }
  return render(request, 'articles/form.html', context)



@login_required
def detail(request, article_pk):
  article = get_object_or_404(Article, pk=article_pk)
  movie = get_object_or_404(Movie, pk=article.movie_title.pk)
  form = CommentForm()
  context = {
    'article': article,
    'movie': movie,
    'form': form,
  }
  return render(request, 'articles/detail.html', context)



@login_required
def update(request, article_pk):
  article = get_object_or_404(Article, pk=article_pk)
  if request.user == article.user:
    if request.method == "POST":
      form = ArticleForm(request.POST, instance=article)
      if form.is_valid():
        updated = form.save()
        return redirect('articles:detail', updated.pk)
    else:
      form = ArticleForm(instance=article)
    context = {
      'form': form,
    }
    return render(request, 'articles/form.html', context)
  else:
    return redirect('articles:detail', article_pk)



@login_required
def delete(request, article_pk):
  article = get_object_or_404(Article, pk=article_pk)
  if request.user == article.user:
    article.delete()
    return redirect('articles:index')
  else:
    return redirect('articles:detail', article_pk)



@login_required
def comment_create(request, article_pk):
  article = get_object_or_404(Article, pk=article_pk)
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.article = article
      comment.user = request.user
      comment.save()
  return redirect('articles:detail', article.pk)



@login_required
def comment_delete(request, article_pk, comment_pk):
  comment = get_object_or_404(Comment, pk=comment_pk)
  if request.user == comment.user:
    comment.delete()
  return redirect('articles:detail', article_pk)



@login_required
def comment_update(request, article_pk, comment_pk):
  comment = get_object_or_404(Comment, pk=comment_pk)
  if request.user == comment.user:
    form = CommentForm(request.POST, instance=comment)
    if request.method == 'POST':
      if form.is_valid():
        form.save()
        return redirect('articles:detail', article_pk)
    else:
      form = CommentForm(instance=comment)
    context = {
      'form': form,
    }
    return render(request, 'articles/form.html', context)
  else:  
    return redirect('articles:detail', article_pk) 



@login_required
def search(request):
  kwd = request.COOKIES['kwd']  # articles/index.html에서 저장한 키워드를 쿠키에서 꺼낸다.
  articles = Article.objects.filter(title__contains=kwd).order_by('-pk') # 키워드를 제목에 포함하는 글 검색해 pk 역순으로 정렬
  
  paginator = Paginator(articles, 15)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'kwd': kwd,
    'articles': articles,
    'page_obj': page_obj,
  }
  return render(request, 'articles/index.html', context)



@login_required
def best(request):
  articles = Article.objects.filter(rank=10).order_by('-pk')

  paginator = Paginator(articles, 15)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'articles': articles,
    'page_obj': page_obj,
  }
  return render(request, 'articles/index.html', context)



@login_required
def worst(request):
  articles = Article.objects.filter(rank=0).order_by('-pk')

  paginator = Paginator(articles, 15)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'articles': articles,
    'page_obj': page_obj,
  }
  return render(request, 'articles/index.html', context)