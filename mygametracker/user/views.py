from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .form import SignupForm, LoginForm
from .models import User


def index(request):
    return HttpResponse("This is the Home Page.")


def logout(request):
    request.session['curr_user'] = ''
    return redirect('user:login')


def dashboard(request):
    user = User.objects.all()
    return render(request, 'dashboard.html', {'users': user})


def profile(request):
    return render(request, 'profile.html')


def friends(request):
    return render(request, 'friends.html')


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
            User.objects.filter(username=username, password=password)
            request.session['curr_user'] = username
            print("Login successful")
            return render(request, 'home.html')
        except:
            error = True
            print("Login failed")
            return render(request, self.template, {'form': login, "response": error})
