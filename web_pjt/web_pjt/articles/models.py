from django.db import models
from django.conf import settings
from movies.models import Movie
import datetime

# Create your models here.
class Article(models.Model):
  movie_title = models.ForeignKey(Movie, on_delete=models.CASCADE)
  rank = models.IntegerField(choices=list(zip(range(0, 11), range(0, 11))))
  title = models.CharField(max_length=100)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)



class Comment(models.Model):
  content = models.CharField(max_length=300)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  article = models.ForeignKey(Article, on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)