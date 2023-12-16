from django.urls import path
from . import views

app_name = 'collection'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:user>/', views.user_collections, name='main'),
    path('<str:user>/<int:collection_id>', views.collection_detail, name='collection_detail'),
]
