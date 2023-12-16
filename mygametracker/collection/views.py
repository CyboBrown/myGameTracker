from django.shortcuts import render, get_object_or_404
from .models import Collection
from user.models import User


def index(request):
    return render(request, 'user_collections.html', {'user': ''})


def user_collections(request, user):
    user_id = User.objects.get(username=user).user_id
    collections = Collection.objects.filter(user_id=user_id)
    return render(request, 'user_collections.html', {'collections': collections, 'user': user})


def collection_detail(request, user, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    return render(request, 'collection_detail.html', {'collection': collection, 'user': user})
