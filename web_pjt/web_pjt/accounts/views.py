from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from articles.models import Article, Comment



def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      auth_login(request, user)
      return redirect('main:index')
  else:
    form = UserCreationForm()
  context = {
    'form': form,
  }
  return render(request, 'accounts/signup.html', context)
      


def login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
      auth_login(request, form.get_user())
      return redirect('main:index')
  else:
    form = AuthenticationForm()
  context = {
    'form': form,
  }
  return render(request, 'accounts/login.html', context)  



@login_required
def logout(request):
  auth_logout(request)
  return redirect('main:index')



@login_required
def myinfo(request):    # 내 정보(내가 작성한 글, 내가 작성한 댓글)를 볼 수 있는 페이지
  user = request.user
  articles = Article.objects.filter(user=user).order_by('-pk')  # 전체 Article에서 작성자가 현재 요청한 유저인 글을 pk 역순으로 받아온다.
  comments = Comment.objects.filter(user=user).order_by('-pk')  # 전체 Comment에서 작성자가 현재 요청한 유저인 댓글을 pk 역순으로 받아온다.

  context = {
    'user': user,
    'articles': articles,
    'comments': comments,
  }
  return render(request, 'accounts/user.html', context)