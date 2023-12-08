from django.db import models
from user.models import User
from game.models import Game


# Create your models here.
class Collection(models.Model):
    collection_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    game_collection = models.ManyToManyField(Game)

    def __str__(self):
        return self
