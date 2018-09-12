"""
Controllers for the Battleship application

"""
from django.core.serializers import serialize
from django.db import DatabaseError, DataError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Game,  Ship, ShipCoordinates

# Create your views here.


@csrf_exempt
def get_post_games(request):
    """
    Creates a new entry in the Games table for a POST request
    Returns all the rows in the Games table for a GET request

    """
    if request.method == 'POST':
        game = Game.objects.create(start_date=timezone.now())
        response = HttpResponse()
        response['location'] = "battleship/api/v1/games/{0}/".format(game.pk)
        return response
    elif request.method == 'GET':
        games_list = Game.objects.all()
        return HttpResponse(serialize('json', games_list))
    else:
        return HttpResponse(status=405)


def get_delete_patch_game(request, game_id):
    """
    Returns a row from the Games table for the given game_id

    """
    if request.method == 'GET':
        game_inst = get_object_or_404(Game, pk=game_id)
        return HttpResponse(serialize('json', game_inst.ship_set.all()))
    elif request.method == 'DELETE':
        game_inst = get_object_or_404(Game, pk=game_id)
        game_inst.delete()
        game_inst.save()
        return HttpResponse('Deleted record with id: {}'.format(game_id))
    elif request.method == 'PATCH':
        update_game_from_req(request)


def get_alive_ships(request, game_id):
    """
    Returns the ships still in the game

    """
    if request.method == 'GET':
        game_inst = get_object_or_404(Game, pk=game_id)
        ships_left = game_inst.ship_set.filter(isalive=True)
        return HttpResponse(serialize('json', ships_left))
    return HttpResponse(status=405)


def get_game_coordinates(request, game_id):
    """
    """
    if request.method == 'GET':
        game_inst = get_object_or_404(Game, pk=game_id)
        game_coordinates = game_inst.shipcoordinates_set.all()
        return HttpResponse(serialize('json', game_coordinates))
    return HttpResponse(status=405)


def get_game_ships(request, game_id):
    """
    """
    if request.method == 'GET':
        game_inst = get_object_or_404(Game, pk=game_id)
        game_ships = game_inst.ship_set.all()
        return HttpResponse(serialize('json', game_ships))
    return HttpResponse(status=405)


def get_post_ships(request):
    """
    """
    if request.method == 'POST':
        


def update_game_from_req(request):
    """
    PATCH verb for the game object

    """
    return HttpResponse('Work in progress')


def get_ships(request):
    """
    """
    if request.method == 'GET':
        all_ships = Ship.objects.all()
        return HttpResponse(serialize('json', all_ships))
    elif request.method == 'POST':

    else:
        return HttpResponse(status=405)


def get_ship_status(request, ship_id):
    """
    Returns the detail of a ship

    """
    if request.method == 'GET':
        ship_inst = get_object_or_404(Ship, pk=ship_id)
        return JsonResponse(ship_inst, safe=False)
    else:
        return HttpResponse(status=405)
