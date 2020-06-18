from django.shortcuts import render
from movies.models import Movie
from articles.models import Article
from datetime import timedelta
import datetime
from django.utils import timezone



def index(request):
  movies = Movie.objects.order_by('-release_date')[:4]
  articles = Article.objects.order_by('-pk')[:5]
  check_now = timezone.now()
  check_delta = timezone.now() - timedelta(hours=6)
  context = {
    'movies': movies,
    'articles': articles,
    'check_now': check_now,
    'check_delta': check_delta,
  }
  return render(request, 'main/main.html', context)