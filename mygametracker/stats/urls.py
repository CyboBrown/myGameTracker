from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'stats'
urlpatterns = [
    path('browse/', views.browse_games, name='browse'),
    path('list/', views.game_list, name='list'),
    path('add_entry/<int:game_id>/', views.add_entry, name='add_entry'),
    path('update_entry/<int:game_id>/', views.update_entry, name='update_entry'),
    path('get_entry_details/<int:game_id>/', views.get_entry_details, name='get_entry_details'),
    path('delete_entry/<int:game_id>/', views.delete_entry, name='delete_entry'),
    path('game/<int:game_id>/', views.game_viewer, name='game_viewer'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
