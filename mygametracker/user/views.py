from django.http import HttpResponse
from .form import SignupForm, LoginForm, UserProfileUpdateForm
from .models import User, UserFriend
from django.shortcuts import render, redirect
from django.views import View


def index(request):
    return HttpResponse("This is the Home Page.")


def logout(request):
    request.session['curr_user'] = ''
    return redirect('user:login')


def dashboard(request):
    user = User.objects.all()
    return render(request, 'dashboard.html', {'users': user})


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
    friends = UserFriend.objects.all()

    if request.method == 'POST':
        friend_username = request.POST.get('friend_username')

        try:
            friend = UserFriend.objects.get(friend_username=friend_username)
            friend.delete()
        except UserFriend.DoesNotExist:
            return redirect('user:friends')

    return render(request, 'friends.html', {'friends': friends})


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
