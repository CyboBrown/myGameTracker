from django.db import IntegrityError, OperationalError
from django.shortcuts import render, redirect
from django.db import connection
from .models import Game


class GameExistsError(Exception):
    pass


def home(request):
    # Retrieve 5 random games using a stored procedure
    with connection.cursor() as cursor:
        cursor.callproc('GetRandomGames', [5])
        games_for_you = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

    # Retrieve 5 games ordered by rating using a stored procedure
    with connection.cursor() as cursor:
        cursor.callproc('GetTopRatedGames', [5])
        games_for_you2 = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

    return render(request, 'home.html', {'games_for_you': games_for_you, 'games_for_you2': games_for_you2})

def add_new_game(request):
    success_message = None
    error_message = None
    info_message = None

    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        description = request.POST.get('description')
        image = request.POST.get('image')
        release_date = request.POST.get('release_date')
        username_credits = request.session.get('curr_user')

        # Assuming you have a user_id available in your session
        if len(image) is 0:
            image = 'http://tinyurl.com/yajp3tyy'
        if username_credits is not None:
            try:
                # Call the stored procedure
                with connection.cursor() as cursor:
                    cursor.callproc('AddNewGame', [title, description, release_date, genre, username_credits, image])

                # Set success message
                success_message = 'Success: New game added.'


            except IntegrityError as e:

                # Check if it's a title already exists error

                if "Error: Title already exists" in str(e):

                    error_message = 'Error: The title already exists. Please choose a different title.'

                else:



                    error_message = f"Error: {str(e)}"


            except OperationalError as e:

                # Handle the specific OperationalError

                error_message = f"Game already exists!"

            except GameExistsError as e:

                error_message = str(e)

        else:
            # Handle the case where user_id is not available
            error_message = "Error: User not logged in"

    return render(request, 'add_new_game.html', {'success_message': success_message, 'error_message': error_message, 'info_message': info_message})

def top_credits(request):
    top_credits_list = []

    with connection.cursor() as cursor:
        cursor.callproc('GetTopCredits', [10])
        top_credits_list = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

    return render(request, 'top_credits.html', {'top_credits_list': top_credits_list})

def games_list(request):
    with connection.cursor() as cursor:
        cursor.callproc('GetAllGames', [])
        games_list = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

    # Order the games alphabetically by title
    games_list = sorted(games_list, key=lambda x: x['title'])

    return render(request, 'games_list.html', {'games_list': games_list})