from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64)
    birthdate = models.DateField(null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=64)
    bio = models.TextField()
    genders = (
        ("M", "Male"),
        ("F", "Female")
    )
    gender = models.CharField(max_length=1, choices=genders)

    def __str__(self):
        return self


class UserFriend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')

    def __str__(self):
        return self
#
