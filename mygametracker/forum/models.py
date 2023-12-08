from django.db import models
from user.models import User
from game.models import Game


# Create your models here.
class Forum(models.Model):
    forum_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField()
    users = models.ManyToManyField(User, related_name='forums_participated')
    games = models.ManyToManyField(Game, through='Discussion')

    def __str__(self):
        return self


class Discussion(models.Model):
    # associative model for games and forum
    discussion_id = models.AutoField(primary_key=True)
    game = models.ForeignKey("game.Game", on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    number_of_posts = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self


class Post(models.Model):
    # individual posts in forums
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self
