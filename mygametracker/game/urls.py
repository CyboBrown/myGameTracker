from django.urls import path
from .views import home, add_new_game  # Import the add_new_game view

app_name = 'game'

urlpatterns = [
    path('', home, name='home'),
    path('add_new_game/', add_new_game, name='add_new_game'),
]
