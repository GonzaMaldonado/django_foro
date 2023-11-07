from django.db import models
from users.models import  User

class Room(models.Model):
  name = models.CharField(max_length=50)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  like = models.ManyToManyField(User, related_name="like", default=None, blank=True)

  class Meta:
    ordering = ['-id']

  @property
  def num_likes(self):
    return self.like.all().count()

  def __str__(self) -> str:
    return self.name


LIKE_CHOICES = (
  ('Like', 'Like'),
  ('Unlike', 'Unlike')
)
class Like(models.Model):
  user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
  room = models.ForeignKey(Room, related_name="room", on_delete=models.CASCADE)
  value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=6)


class Message(models.Model):
  room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
  user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
  content = models.TextField()