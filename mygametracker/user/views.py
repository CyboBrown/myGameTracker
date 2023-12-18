from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .form import SignupForm, LoginForm, AddFriendForm, UserProfileUpdateForm
from .models import User, UserFriend
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View


def index(request):
    return HttpResponse("This is the Home Page.")


def logout(request):
    request.session['curr_user'] = ''
    return redirect('user:login')


def dashboard(request):
    user = User.objects.all()
    return render(request, 'dashboard.html', {'users': user})


# def profile(request):
#     # Retrieve user ID from the session
#     user_id = request.session.get('curr_user_id')
#
#     # Get the user instance from the database
#     user = get_object_or_404(User, pk=user_id)
#
#     # Access fields from the user instance
#     username = user.username
#     join_date = user.join_date
#     email = user.email
#     bio = user.bio
#     gender = user.gender
#
#     return render(request, 'profile.html', {
#         'username': username,
#         'join_date': join_date,
#         'email': email,
#         'bio': bio,
#         'gender': gender,
#     })


def profile(request):
    current_username = request.session.get('curr_user', None)

    if current_username:
        try:
            user = User.objects.get(username=current_username)
        except User.DoesNotExist:
            return HttpResponse("User does not exist")

        if request.method == 'POST':
            form = UserProfileUpdateForm(request.POST)

            if form.is_valid():
                new_username = form.cleaned_data['new_username']
                new_password = form.cleaned_data['new_password']
                new_email = form.cleaned_data['new_email']
                new_bio = form.cleaned_data['new_bio']
                new_gender = form.cleaned_data['new_gender']

                user.username = new_username
                user.password = new_password
                user.email = new_email
                user.bio = new_bio
                user.gender = new_gender
                user.save()

                return redirect('user:login')
        else:
            form = UserProfileUpdateForm()

        return render(request, 'profile.html', {'user': user, 'form': form})
    else:
        return HttpResponse("User not authenticated")

def delete_profile(request):
    if request.method == 'POST':
        current_username = request.session.get('curr_user')

        if current_username:
            try:
                user = User.objects.get(username=current_username)
                user.delete()

                request.session.clear()

                return redirect('user:logout')
            except User.DoesNotExist:
                return HttpResponse("User does not exist")
        else:
            pass
    else:
        pass


def friends(request):
    return render(request, 'friends.html')


class AddFriend(View):
    template = 'friends.html'

    def get(self, request, user):
        user_id = User.objects.get(username=user).user_id
        friends = UserFriend.objects.filter(user_id=user_id)
        form = AddFriendForm()
        return render(request, 'friends.html', {'friends': friends, 'user': user, 'form': form})

    def post(self, request, user):
        user_id = User.objects.get(username=user).user_id
        friends = UserFriend.objects.filter(user_id=user_id)

        form = AddFriendForm(request.POST)
        if form.is_valid():
            friend_id = form.cleaned_data['friend']
            friend_user = User.objects.get(user_id=friend_id)  # Get the User instance

            if not UserFriend.objects.filter(user_id=user_id, friend=friend_user).exists():
                friend = form.save(commit=False)
                friend.user_id = User.objects.get(user_id=user_id)
                friend.friend = friend_user  # Assign the User instance to the friend field
                friend.save()

                # Redirect after successful form submission
                return render(request, self.template, {'friends': friends, 'user': user, 'form': form})

            form.add_error('friend', 'This user is already a friend.')

        return render(request, self.template, {'friends': friends, 'user': user, 'form': form})


# class AddFriend(View):
#     template = 'friends.html'
#
#     def get(self, request, user):
#         user_id = User.objects.get(username=user).user_id
#         friend = UserFriend.objects.filter(user_id=user_id)
#         form = AddFriendForm()
#         return render(request, 'friends.html', {'friends': friend, 'user': user, 'form': form})
#
#     def post(self, request, user):
#         user_id = User.objects.get(username = user).user_id
#         friend = UserFriend.objects.filter(user_id = user_id)
#
#         form = AddFriendForm(request.POST)
#         if form.is_valid():
#             if not UserFriend.objects.filter(user_id = user_id, friend = friend).exists():
#                 friend = form.save(commit=False)
#                 friend.user_id = User.objects.get(user_id = user_id)
#                 friend.save()
#
#                 # Redirect after successful form submission
#                 return render(request, self.template, {'friends': friend, 'user': user, 'form': form})
#
#             form.add_error('name', 'A collection with this name already exists.')
#
#         return render(request, self.template, {'friends': friend, 'user': user, 'form': form})

class UserSignup(View):
    template = 'signup.html'

    def get(self, request):
        user = SignupForm()
        return render(request, self.template, {'form': user})

    def post(self, request):
        user = SignupForm()
        error = False
        if request.method == 'POST':
            user = SignupForm(request.POST)
            if user.is_valid():
                if len(User.objects.filter(username=request.POST.get('username'),
                                           email=request.POST.get('email'))) == 0:
                    user.save()
                    return render(request, 'login.html', {'form': LoginForm()})
                else:
                    error = True
                    return render(request, self.template, {'form': user, 'response': error})
        return render(request, self.template, {'form': user, 'response': error})


# class UserLogin(View):
#     template = 'login.html'
#
#     def get(self, request):
#         login = LoginForm()
#         return render(request, self.template, {'form': login})
#
#     def post(self, request):
#         login = LoginForm()
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         error = False
#         try:
#             User.objects.filter(username=username, password=password)
#             request.session['curr_user'] = username
#             print("Login successful")
#             return render(request, 'home.html')
#         except:
#             error = True
#             print("Login failed")
#             return render(request, self.template, {'form': login, "response": error})

class UserLogin(View):
    template = 'login.html'

    def get(self, request):
        login = LoginForm()
        return render(request, self.template, {'form': login})

    def post(self, request):
        login = LoginForm()
        username = request.POST.get("username")
        password = request.POST.get("password")
        error = False
        try:
            user = User.objects.get(username=username, password=password)
            request.session['curr_user'] = username
            print("Login successful")
            return render(request, 'home.html')
        except User.DoesNotExist:
            error = True
            print("Login failed")
            return render(request, self.template, {'form': login, "response": error})
