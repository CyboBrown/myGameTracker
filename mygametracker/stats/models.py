from django.db import models
from user.models import User
from game.models import Game


# Create your models here.
class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    platform = models.CharField(max_length=64)

    def __str__(self):
        return self


class UserGamePlatform(models.Model):
    STATUS_CHOICES = [
        ("PTP", "Planning to Play"),
        ("OH", "On Hold"),
        ("CP", "Currently Playing"),
        ("COM", "Completed"),
        ("DR", "Dropped"),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform_id = models.ForeignKey(Platform, on_delete=models.CASCADE)
    rating_int = models.IntegerField(name="score")
    # progress_int = models.IntegerField(name="Progress")
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    review = models.TextField()

    # String return to be decided, for now, just return object reference.
    def __str__(self):
        return self


