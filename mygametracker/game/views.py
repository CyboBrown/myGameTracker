from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.db import connection
from .models import Game



# Define the custom exception
class GameExistsError(Exception):
    pass


def home(request):
    # Retrieve 5 random games from the database
    games_for_you = Game.objects.all().order_by('?')[:5]
    games_for_you2 = Game.objects.all().order_by('-rating')[:5]

    return render(request, 'home.html', {'games_for_you': games_for_you,'games_for_you2': games_for_you2})


def add_new_game(request):
    success_message = None
    error_message = None

    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        description = request.POST.get('description')
        release_date = request.POST.get('release_date')

        # Assuming you have a user_id available in your session
        user_id = 1

        if user_id is not None:
            try:
                # Call the stored procedure
                with connection.cursor() as cursor:
                    cursor.callproc('AddNewGame', [title, description, release_date, genre, user_id])

                # Set success message
                success_message = 'Success: New game added.'

            except IntegrityError as e:
                # Print the exact error message for investigation
                print(f"IntegrityError: {e}")

                # Check if it's a title already exists error
                if "Error: Title already exists" in str(e):
                    raise GameExistsError("Error: Title already exists")

                # Handle other integrity errors (e.g., user_id is null)
                error_message = f"Error: {str(e)}"

            except GameExistsError as e:
                # Handle the custom exception (title already exists)
                error_message = str(e)

        else:
            # Handle the case where user_id is not available
            error_message = "Error: User not logged in"

    return render(request, 'add_new_game.html', {'success_message': success_message, 'error_message': error_message})
