from django.db import connection
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Collection
from .forms import CollectionForm
from user.models import User


def index(request):
    return render(request, 'user_collections.html', {'user': ''})


def collection_detail(request, user, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    return render(request, 'collection_detail.html', {'collection': collection, 'user': user})


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

                # Redirect after successful form submission
                return render(request, self.template, {'collections': collections, 'user': user, 'form': form})

            form.add_error('name', 'A collection with this name already exists.')

        return render(request, self.template, {'collections': collections, 'user': user, 'form': form})
