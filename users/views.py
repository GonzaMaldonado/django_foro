from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import User
from foro.models import Room
from .forms import RegisterForm, UpdateUserForm

class Login(generic.View):

  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('home')
    return render(request, 'users/login.html')
    
  def post(self, request, *args, **kwargs):
    username = self.request.POST.get('username')
    password = self.request.POST.get('password')

    try:
      user = User.objects.get(username=username)
    except:
      messages.success(request, 'User does not exist')
      return redirect('login')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      messages.success(request, f'Welcome back {user.username}!')
      return redirect('home')
    
    messages.success(request, 'Username or password does not match!')
    return redirect('login')


class Register(generic.View):

  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('home')
    return render(request, 'users/register.html', {'form': RegisterForm})
    
  def post(self, request, *args, **kwargs):  
    form = RegisterForm(request.POST)
    
    if form.is_valid():
      user = form.save(commit=False)
      user.email = user.email.lower()
      user.save()
      login(request, user)
      messages.success(request, f'Welcome {user.username}')
      return redirect('home')

    error_text = form.errors.as_text()
    error = error_text.split('*')
    messages.success(request, f'{error[2]}')
    return redirect('register')


@method_decorator(login_required, name='dispatch')
class Logout(generic.View):

  def get(self, request, *args, **kwargs):
    logout(request)
    messages.success(request, 'See you later!')
    return redirect('login')


@method_decorator(login_required, name='dispatch')
class MyProfile(generic.View):

  def get(self, request, *args, **kwargs):
    user = request.user
    rooms = user.room_set.all()
    return render(request, 'users/my_profile.html', {'rooms': rooms})


@method_decorator(login_required, name='dispatch')
class UpdateProfile(generic.View):

  def get(self, request, *args, **kwargs):
    form = UpdateUserForm(instance=request.user)
    return render(request, 'users/update_profile.html', {'form': form})
  
  def post(self, request):
    user = request.user
    form = UpdateUserForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
      form.save()
      messages.success(request, 'Profile Updated')
      return redirect('my_profile')
    messages.succes(request, 'Ups... Something went wrong!')
  
  
@method_decorator(login_required, name='dispatch')
class Profiles(generic.View):

  def get(self, request, pk, *args, **kwargs):
    user = User.objects.get(pk=pk)
    rooms = Room.objects.filter(user=user.id)
    return render(request, 'users/profiles.html', {'user': user, 'rooms': rooms})