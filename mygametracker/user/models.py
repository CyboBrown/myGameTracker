from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64)
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

    def update_profile(self, new_username,new_password ,new_email, new_bio, new_gender):
        self.username = new_username
        self.password = new_password
        self.email = new_email
        self.bio = new_bio
        self.gender = new_gender
        self.save()


class UserFriend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')
    friend_username = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.friend_username)

