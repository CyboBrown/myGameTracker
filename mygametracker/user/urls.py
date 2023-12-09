from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.index, name='home'),
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
]
