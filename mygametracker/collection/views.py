from django.db import connection
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Collection
from .forms import CollectionForm
from user.models import User
from stats.models import UserGamePlatform


def index(request):
    return render(request, 'user_collections.html', {'user': ''})


def collection_detail(request, user, collection_id):
    # collection = get_object_or_404(Collection, pk=collection_id)
    user_id = User.objects.get(username=user).user_id
    collection = get_object_or_404(Collection, pk=collection_id, user_id=user_id)
    games = collection.game_collection.all()
    game_details = UserGamePlatform.objects.filter(user_id=user_id, game_id__in=games).distinct()
    return render(request, 'collection_detail.html', {'collection': collection, 'user': user, 'games': games, 'game_details': game_details})


def delete_collection(request, user, collection_id):
    user_object = User.objects.get(username=request.session['curr_user'])
    collections = Collection.objects.filter(user_id=user_object.user_id)
    form = CollectionForm()
    collection = get_object_or_404(Collection, pk=collection_id)
    if user_object == collection.user_id:
        collection.delete()
        messages.success(request, 'Collection deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this collection.')
    return render(request, 'user_collections.html', {'collections': collections, 'user': user, 'form': form})


def update_collection(request, user, collection_id):
    user_id = User.objects.get(username=user).user_id
    collections = Collection.objects.filter(user_id=user_id)
    form = CollectionForm()
    collection = get_object_or_404(Collection, pk=collection_id, user_id=user_id)
    if request.method == 'POST':
        collection.name = request.POST.get('txtCollectionName')
        collection.description = request.POST.get('txtDescription')
        if request.POST.get('cbPrivate') == 'on':
            collection.is_private = 1
        else:
            collection.is_private = 0
        collection.save()
        messages.success(request, 'Collection updated successfully.')
    return render(request, 'user_collections.html', {'collections': collections, 'user': user, 'form': form})


class CreateCollection(View):
    template = 'user_collections.html'

    def get(self, request, user):
        user_id = User.objects.get(username=user).user_id
        collections = Collection.objects.filter(user_id=user_id)
        form = CollectionForm()
        return render(request, 'user_collections.html', {'collections': collections, 'user': user, 'form': form})

    def post(self, request, user):
        user_id = User.objects.get(username=user).user_id
        collections = Collection.objects.filter(user_id=user_id)
        form = CollectionForm(request.POST)
        if form.is_valid():
            if not Collection.objects.filter(name=form.cleaned_data['name'], user_id=user_id).exists():
                collection = form.save(commit=False)
                collection.user_id = User.objects.get(username=user)
                collection.save()
                messages.success(request, 'Collection added successfully.')
                return render(request, self.template, {'collections': collections, 'user': user, 'form': form})
            messages.error(request, 'A collection with this name already exists.')
        return render(request, self.template, {'collections': collections, 'user': user, 'form': form})
