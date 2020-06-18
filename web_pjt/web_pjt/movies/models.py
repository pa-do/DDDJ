from django.db import models
from django.conf import settings

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__ (self):
      return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    overview = models.TextField()
    original_language = models.CharField(max_length=20)
    poster_path = models.CharField(max_length=500)
    backdrop_path = models.CharField(max_length=500)
    genres = models.ManyToManyField(Genre)

    def __str__ (self):
      return self.title