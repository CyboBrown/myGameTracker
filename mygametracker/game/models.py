from django.db import models
# from stats.models import Platform


# Create your models here.
class Developer(models.Model):
    developer_id = models.AutoField(primary_key=True)
    developer = models.CharField(max_length=64)

    def __str__(self):
        return self


class Publisher(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    publisher = models.CharField(max_length=64)

    def __str__(self):
        return self


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=64)

    def __str__(self):
        return self


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    release_date = models.DateField()
    platforms = models.ManyToManyField("stats.Platform")
    publishers = models.ManyToManyField(Publisher)
    developers = models.ManyToManyField(Developer)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self
