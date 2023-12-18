from django.urls import path
from . import views

app_name = 'collection'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:user>/', views.CreateCollection.as_view(), name='main'),
    path('<str:user>/delete/<int:collection_id>', views.delete_collection, name='delete'),
    path('<str:user>/edit/<int:collection_id>', views.update_collection, name='edit'),
    path('<str:user>/<int:collection_id>', views.collection_detail, name='collection_detail'),
]
