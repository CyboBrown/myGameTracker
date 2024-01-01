from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from user.models import User
from game.models import Game

from .models import UserGamePlatform


# Create your views here.
def browse_games(request):
    games = Game.objects.all().order_by('title')

    return render(request, 'games.html', {'games': games})


def game_viewer(request, game_id):
    game = get_object_or_404(Game, game_id=game_id)
    user = User.objects.get(user_id=int(request.session.get('curr_user_id')))

    already_added = UserGamePlatform.objects.filter(user_id=int(request.session.get('curr_user_id')), game_id=game_id).exists()

    try:
        entry_id = UserGamePlatform.objects.get(user_id=user, game_id=game)
    except:
        entry_id = 0
        print("Entry does not exist.")

    return render(request, 'game_viewer.html', {'entry_id': entry_id, 'game': game, 'already_added': already_added})


def game_list(request):
    # User mapping stuff, get essential user information behind the scenes.
    current_user = request.session.get('curr_user')
    current_user_id = request.session.get('curr_user_id')

    com_games = UserGamePlatform.objects.filter(user_id_id=current_user_id, status='COM')
    cp_games = UserGamePlatform.objects.filter(user_id_id=current_user_id, status='CP')
    oh_games = UserGamePlatform.objects.filter(user_id_id=current_user_id, status='OH')
    ptp_games = UserGamePlatform.objects.filter(user_id_id=current_user_id, status='PTP')
    dr_games = UserGamePlatform.objects.filter(user_id_id=current_user_id, status='DR')

    all_games_count = UserGamePlatform.objects.filter(user_id_id=current_user_id).count()
    com_games_count = com_games.count()
    cp_games_count = cp_games.count()
    oh_games_count = oh_games.count()
    ptp_games_count = ptp_games.count()
    dr_games_count = dr_games.count()

    return render(request, 'game_list.html', {
        'user': current_user,
        'user_id': current_user_id,
        'com_list': com_games,
        'cp_list': cp_games,
        'oh_list': oh_games,
        'ptp_list': ptp_games,
        'dr_list': dr_games,
        'all_cnt': all_games_count,
        'com_cnt': com_games_count,
        'cp_cnt': cp_games_count,
        'oh_cnt': oh_games_count,
        'ptp_cnt': ptp_games_count,
        'dr_cnt': dr_games_count,
    })


def get_entry_details(request, game_id):
    try:
        # I am gonna fucking kill myself with this naming schemes, WHAT THE HELL IS WHAT??!!
        user = User.objects.get(user_id=int(request.session.get('curr_user_id')))
        entry_id = game_id

        game_entry = UserGamePlatform.objects.get(user_id=user, id=entry_id)
        current_status = ""
        current_score = ""

        # Oh boy, why did we settle for this crap.
        match game_entry.status:
            case "CP":
                current_status = "Currently Playing"
            case "COM":
                current_status = "Completed"
            case "OH":
                current_status = "On Hold"
            case "PTP":
                current_status = "Planning to Play"
            case "DR":
                current_status = "Dropped"

        match game_entry.score:
            case 10:
                current_score = "(10) Masterpiece"
            case 9:
                current_score = "(9) Excellent"
            case 8:
                current_score = "(8) Very Good"
            case 7:
                current_score = "(7) Good"
            case 6:
                current_score = "(6) Fine"
            case 5:
                current_score = "(5) Average"
            case 4:
                current_score = "(4) Bad"
            case 3:
                current_score = "(3) Very Bad"
            case 2:
                current_score = "(2) Horrible"
            case 1:
                current_score = "(1) Unplayable"
            case _:
                current_score = "Undecided"

        # Return details as a JSON response
        entry_details = {
            'status': current_status,
            'rating': current_score,
            'review': game_entry.review,
        }

        return JsonResponse(entry_details)

    except UserGamePlatform.DoesNotExist:
        return JsonResponse({'error': 'An exception has occurred.'}, status=404)


@csrf_exempt
def add_entry(request, game_id):
    if request.method == 'POST':
        current_user = User.objects.get(user_id=request.session.get('curr_user_id'))
        current_game = Game.objects.get(game_id=game_id)
        new_entry = UserGamePlatform(user_id=current_user, game_id=current_game, status="CP", score=0)

        new_entry.save()
        message = "Game added to your list."

        return JsonResponse({'message': message})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def update_entry(request, game_id):
    if request.method == 'POST':
        # Extract data from the POST request
        new_status = request.POST.get('new_status', '')
        new_score = request.POST.get('new_score', '')
        new_review = request.POST.get('new_review', '')
        score = 0

        print(new_score)
        # Fetch the entry from the database
        entry = UserGamePlatform.objects.get(pk=game_id)

        match new_status:
            case "Currently Playing":
                new_status = "CP"
            case "Completed":
                new_status = "COM"
            case "On Hold":
                new_status = "OH"
            case "Planning to Play":
                new_status = "PTP"
            case "Dropped":
                new_status = "DR"

        match new_score:
            case "(10) Masterpiece":
                score = 10
            case "(9) Excellent":
                score = 9
            case "(8) Very Good":
                score = 8
            case "(7) Good":
                score = 7
            case "(6) Fine":
                score = 6
            case "(5) Average":
                score = 5
            case "(4) Bad":
                score = 4
            case "(3) Very Bad":
                score = 3
            case "(2) Horrible":
                score = 2
            case "(1) Unplayable":
                score = 1
            case "Undecided":
                score = 0

        # Update the entry with the new data
        entry.status = new_status
        entry.score = score
        entry.review = new_review
        entry.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def delete_entry(request, game_id):
    if request.method == 'POST':
        try:
            # Fetch the entry from the database and delete it
            entry = UserGamePlatform.objects.get(pk=game_id)
            entry.delete()
            return JsonResponse({'success': True})
        except UserGamePlatform.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Entry not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
