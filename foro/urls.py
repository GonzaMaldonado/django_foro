from django.urls import path
from .views import Home, Rooms, CreateRoom, UpdateRoom, DeleteRoom, Search, LikeView

urlpatterns = [
  path('search/', Search.as_view(), name='search'),
  path('', Home.as_view(), name='home'),
  path('room/<int:pk>/', Rooms.as_view(), name='room'),
  path('create_room/', CreateRoom.as_view(), name='create_room'),
  path('update_room/<int:pk>/', UpdateRoom.as_view(), name='update_room'),
  path('delete_room/<int:pk>/', DeleteRoom.as_view(), name='delete_room'),
  path('like/', LikeView.as_view(), name='like_room'),
]