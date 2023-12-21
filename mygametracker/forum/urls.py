from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='main'),
    path('create/', views.create_forum, name='create_forum'),
    path('<int:forum_id>/', views.forum_details, name='forum_details'),
    path('<int:forum_id>/update/', views.update_forum, name='update_forum'),
    path('forums/<int:forum_id>/create_post/', views.create_post, name='create_post'),
    path('update_post/<int:post_id>/', views.UpdatePostView.as_view(), name='update_post'),
]
