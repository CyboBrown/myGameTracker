from django.db import models
from user.models import User
from game.models import Game


class Collection(models.Model):
    collection_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    is_private = models.BooleanField(default=False)
    types = (
        (0, "Normal"),
        (1, "Favorite"),
        (2, "Owned"),
        (3, "Playing"),
        (4, "Completed"),
    )
    type = models.IntegerField(choices=types, default=0)
    game_collection = models.ManyToManyField(Game)

    def __str__(self):
        return self.name
