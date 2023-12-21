from django.urls import path
from .views import home, add_new_game, top_credits, games_list

app_name = 'game'

urlpatterns = [
    path('', home, name='home'),
    path('add_new_game/', add_new_game, name='add_new_game'),
    path('top_credits/', top_credits, name='top_credits'),
    path('games_list/', games_list, name='games_list'),
]
