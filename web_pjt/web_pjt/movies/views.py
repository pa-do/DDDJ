from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Genre
from articles.models import Article, Comment
from articles.forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import operator
from datetime import timedelta
import datetime
from django.utils import timezone



def index(request):
  # 최신 영화가 앞에 나오도록 한다.
  movies = Movie.objects.order_by('-release_date')
  
  paginator = Paginator(movies, 20)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'movies': movies,
    'page_obj': page_obj,
  }
  return render(request, 'movies/index.html', context)



def movie_genre(request, genre_pk):
  genre = get_object_or_404(Genre, pk=genre_pk)
  # 영화를 장르별로, 인기가 많고 최신에 나온 것 순으로 출력한다.
  movies = genre.movie_set.order_by('-popularity', '-release_date')

  paginator = Paginator(movies, 20)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    'genre': genre,
    'movies': movies,
    'page_obj': page_obj,
  }
  return render(request, 'movies/index.html', context)



@login_required
def movie_articles(request, movie_pk):
  movie = get_object_or_404(Movie, pk=movie_pk)
  articles = Article.objects.filter(movie_title=movie).order_by('-pk')
  check_now = timezone.now()
  check_delta = timezone.now() - timedelta(hours=6)
  
  paginator = Paginator(articles, 20)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'movie': movie,
    'articles': articles,
    'page_obj': page_obj,
    'check_delta' : check_delta,
    'check_now' : check_now,
  }
  return render(request, 'articles/index.html', context)



@login_required
def movie_articles_create(request, movie_pk):
  movie = get_object_or_404(Movie, pk=movie_pk)
  if request.method == 'POST':
    form = ArticleForm(request.POST)
    if form.is_valid():
      article = form.save(commit=False)
      article.user = request.user
      article.save()
      return redirect('movies:movie_articles_detail', movie_pk, article.pk)
  else:
    form = ArticleForm(initial={'movie_title':movie})
  context = {
    'form': form,
  }
  return render(request, 'articles/form.html', context)



@login_required
def movie_articles_detail(request, movie_pk, article_pk):
  article = get_object_or_404(Article, pk=article_pk)
  movie = get_object_or_404(Movie, pk=movie_pk)
  form = CommentForm()
  context = {
    'movie': movie,
    'article': article,
    'form': form,
  }
  return render(request, 'articles/detail.html', context)



@login_required
def movie_articles_update(request, movie_pk, article_pk):
  article = get_object_or_404(Article, pk=article_pk)
  if request.user == article.user:
    if request.method == "POST":
      form = ArticleForm(request.POST, instance=article)
      if form.is_valid():
        form.save()
        return redirect('movies:movie_articles_detail', movie_pk, article_pk)
    else:
      form = ArticleForm(instance=article)
    context = {
      'form': form,
    }
    return render(request, 'articles/form.html', context)
  else:
    return redirect('movies:movie_articles_detail', movie_pk, article_pk)



@login_required
def movie_articles_delete(request, movie_pk, article_pk):
  article = get_object_or_404(Article, pk=article_pk)
  if request.user == article.user:
    article.delete()
    return redirect('movies:movie_articles', movie_pk)
  else:
    return redirect('movies:movie_articles_detail', movie_pk, article_pk)



@login_required
def movie_comment_create(request, movie_pk, article_pk):
  article = get_object_or_404(Article, pk=article_pk)
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.article = article
      comment.user = request.user
      comment.save()
  return redirect('movies:movie_articles_detail', movie_pk, article_pk)



@login_required
def movie_comment_update(request, movie_pk, article_pk, comment_pk):
  comment = get_object_or_404(Comment, pk=comment_pk)
  if request.user == comment.user:
    form = CommentForm(request.POST, instance=comment)
    if request.method == 'POST':
      if form.is_valid():
        form.save()
        return redirect('movies:movie_articles_detail', movie_pk, article_pk)
    else:
      form = CommentForm(instance=comment)
    context = {
      'form': form,
    }
    return render(request, 'articles/form.html', context)
  else:  
    return redirect('movies:movie_articles_detail', movie_pk, article_pk) 



@login_required
def movie_comment_delete(request, movie_pk, article_pk, comment_pk):
  comment = get_object_or_404(Comment, pk=comment_pk)
  if request.user == comment.user:
    comment.delete()
  return redirect('movies:movie_articles_detail', movie_pk, article_pk)



@login_required
def recommend(request): 
  gdict = {12: 0, 14: 0, 16: 0, 18: 0, 27: 0, 28: 0, 35: 0, 36: 0, 37: 0, 53: 0, 80: 0, 
          99: 0, 878: 0, 9648: 0, 10402: 0, 10749: 0, 10751: 0, 10752: 0, 10770: 0}

  # 유저가 작성한 아티클을 기반으로, 각 아티클에 매긴 점수를 영화가 속한 장르에 각각 더해준다.
  articles = Article.objects.filter(user=request.user)
  for article in articles:
    movie = get_object_or_404(Movie, pk=article.movie_title.pk)
    for genre in movie.genres.all():
      gdict[genre.pk] += article.rank
  
  maxi = max(gdict.items(), key=operator.itemgetter(1))[0]

  if gdict[maxi] == 0:
    movies = Movie.objects.order_by('-popularity')[:20]
  else:
    genre = get_object_or_404(Genre, pk=maxi)
    movies = genre.movie_set.order_by('-popularity', '-release_date')[:20]

  paginator = Paginator(movies, 20)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    'movies': movies,
    'page_obj': page_obj,
  }
  return render(request, 'movies/index.html', context)



@login_required
def search(request):
  kwd = request.COOKIES['kwd']
  movies = Movie.objects.filter(title__contains=kwd)
  
  paginator = Paginator(movies, 20)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'kwd': kwd,
    'movies': movies,
    'page_obj': page_obj,
  }
  return render(request, 'movies/index.html', context)



@login_required
def search(request):
  kwd = request.COOKIES['kwd']
  movies = Movie.objects.filter(title__contains=kwd)
  
  paginator = Paginator(movies, 20)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'kwd': kwd,
    'movies': movies,
    'page_obj': page_obj,
  }
  return render(request, 'movies/index.html', context)
