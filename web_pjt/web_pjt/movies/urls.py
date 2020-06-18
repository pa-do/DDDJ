from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
  path('', views.index, name='index'),
  path('<int:genre_pk>/genre/', views.movie_genre, name='movie_genre'),
  path('<int:movie_pk>/articles/', views.movie_articles, name='movie_articles'),
  path('<int:movie_pk>/articles/create/', views.movie_articles_create, name='movie_articles_create'),
  path('<int:movie_pk>/articles/<int:article_pk>/', views.movie_articles_detail, name='movie_articles_detail'),
  path('<int:movie_pk>/articles/<int:article_pk>/update', views.movie_articles_update, name='movie_articles_update'),
  path('<int:movie_pk>/articles/<int:article_pk>/delete/', views.movie_articles_delete, name='movie_articles_delete'),
  path('<int:movie_pk>/articles/<int:article_pk>/comment/', views.movie_comment_create, name='movie_comment_create'),
  path('<int:movie_pk>/articles/<int:article_pk>/comment/<int:comment_pk>/update/', views.movie_comment_update, name='movie_comment_update'),
  path('<int:movie_pk>/articles/<int:article_pk>/comment/<int:comment_pk>/delete/', views.movie_comment_delete, name='movie_comment_delete'),
  path('recommend/', views.recommend, name='recommend'),
  path('search/', views.search, name='search'),
]
