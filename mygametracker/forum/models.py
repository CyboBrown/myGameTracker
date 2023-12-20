from django.db import models
from django.utils import timezone
from user.models import User
from game.models import Game


# Create your models here.
class Forum(models.Model):
    forum_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    game = models.ManyToManyField(Game, through='GameForumRelationship')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) # add user that created the forum
    post_count = models.PositiveIntegerField(default=0)
    _original_title = None
    _original_description = None

    def save(self, *args, **kwargs):
        if self.pk is None:
            self._original_title = self.title
            self._original_description = self.description
        else:
            if self.title != self._original_title or self.description != self._original_description:
                self.last_updated = timezone.now()

        super().save(*args, **kwargs)

    def update_forum_stats(self):
        self.post_count = self.post_set.count()

        latest_post = self.post_set.order_by('-posted_on').first()

        if latest_post:
            self.last_updated = latest_post.posted_on
        else:
            self.last_updated = self.created_on

        if self.title != self._original_title or self.description != self._original_description:
            self.last_updated = timezone.now()

        self.save()

    def __str__(self):
        return self.title


class Post(models.Model):
    # individual posts in forums
    post_id = models.AutoField(primary_key=True)
    content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    _original_content = None

    def save(self, *args, **kwargs):
        if self.pk is None:
            self._original_content = self.content
        else:
            if self.content != self._original_content:
                self.last_updated = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self


class GameForumRelationship(models.Model):
    # to have a many-to-many relationship between game and forum
    # without touching the game model (not my part)
    gameforum_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)

    def __str__(self):
        return self


class UserForumParticipation(models.Model):
    # associative model for user participation in forums
    userforum_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self