from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('friends/', views.friends, name='friends'),
    path('add_friend/', views.add_friend, name='add_friend'),
]
