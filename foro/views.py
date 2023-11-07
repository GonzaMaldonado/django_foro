from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from users.models import User
from .models import Room, Like, Message
from .forms import RoomForm

@method_decorator(login_required, name='dispatch')
class Home(View):
  def get(self, request):
    user = request.user
    users= User.objects.exclude(username=user.username)[:5]
    rooms = Room.objects.all()
    likes = user.like.all()

    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'foro/home.html', {'page_obj': page_obj, 'users': users, 'likes': likes})


@method_decorator(login_required, name='dispatch')
class Rooms(View):
  def get(self, request, pk, *args, **kwargs):
    room = Room.objects.get(pk=pk)
    m = Message.objects.filter(room=room)
    return render(request, 'foro/room.html', {'room': room, 'm': m})


@method_decorator(login_required, name='dispatch')
class CreateRoom(View):
  def get(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return redirect('login')
    return render(request, 'foro/create_room.html', {'form': RoomForm})
    
  def post(self, request, *args, **kwargs):
    form = RoomForm(request.POST)
    
    if form.is_valid():
      room = form.save(commit=False)
      room.user = request.user
      room.save()
      messages.success(request, f'Room {room.name} created!')
      return redirect('home')

    error_text = form.errors.as_text()
    error = error_text.split('*')
    messages.success(request, f'{error[2]}')
    return redirect('room')


@method_decorator(login_required, name='dispatch')
class UpdateRoom(View):
  def get(self, request, pk, *args, **kwargs):
    room = Room.objects.get(pk=pk)
    form = RoomForm(instance=room)
    return render(request, 'foro/update_room.html', {'form': form})
  
  def post(self, request, pk):
    room = Room.objects.get(pk=pk)
    if request.user == room.user:
      form = RoomForm(request.POST or None, instance=room)
      if form.is_valid():
        form.save()
        messages.success(request, 'Room updated!')
        return redirect('my_profile')
    messages.succes(request, "Upps... you don't own this room")
    return redirect('home')


@method_decorator(login_required, name='dispatch')
class DeleteRoom(View):
  def get(self, request, pk):
    room = Room.objects.get(pk=pk)
    if request.user == room.user:
      room.delete()
      messages.success(request, 'Room deleted.')
      return redirect('my_profile')
    messages.success(request, 'Ups... You dont own this room!')
    return redirect('home')


@method_decorator(login_required, name='dispatch') 
class Search(View):
  def get(self, request, *args, **kwargs):
    query = request.GET.get('query', '')
    rooms =  Room.objects.filter(name__icontains=query)
    return render(request, 'foro/search.html', {'query': query, 'rooms': rooms})


@method_decorator(login_required, name='dispatch')
class LikeView(View):
  def post(self, request, *args, **kwargs):
    user = request.user
    room_id = request.POST.get('room_id')
    room_obj = Room.objects.get(id=room_id)

    if user in room_obj.like.all():
      room_obj.like.remove(user)
    else:
      room_obj.like.add(user)

    like, created = Like.objects.get_or_create(user=user, room_id=room_id)

    if not created:
      if like.value == 'Like':
        like.value = 'Unlike'
      else:
        like.value = 'Like'
    
    like.save()
    return HttpResponseRedirect((request.META.get('HTTP_REFERER')))