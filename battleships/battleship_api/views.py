"""
Controllers for the Battleship application

"""
import json

from django.core.serializers import serialize
from django.db import DatabaseError, DataError
from django.http import (Http404, HttpRequest, HttpResponse,
                         HttpResponseBadRequest, HttpResponseNotAllowed,
                         HttpResponseServerError)
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Game, Ship, ShipCoordinates
from .serializers import (GameSerializer, ShipCoordinatesSerializer,
                          ShipSerializer)

# Create your views here.


class GameList(APIView):
    """
    List all games, or create a new Game

    """
    queryset = Game.objects.all()

    def get(self, request, format=None):
        """
        """
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        """
        # serializer = GameSerializer(data=request.data)
        data = {
            'start_date': timezone.now(),
        }
        serializer = GameSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return HttpResponseNotAllowed()


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
        ships_left = game_inst.ship_set.filter(is_alive=True)
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


def get_post_game_ships(request, game_id):
    """
    """
    game_inst = get_object_or_404(Game, pk=game_id)
    if request.method == 'GET':
        game_ships = game_inst.ship_set.all()
        return HttpResponse(serialize('json', game_ships))
    elif request.method == 'POST':
        game_inst.rand_init_ships()
        ships_created = game_inst.ship_set.all().count()
        data = {
            'shipsCreated': ships_created,
        }
        return JsonResponse(data=data, status=201)
    else:
        return HttpResponse(status=405)


def get_post_ships(request):
    """
    """
    pass


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
    else:
        return HttpResponse(status=405)


def get_ship_coordinates(request, ship_id):
    """
    """
    if request.method == 'GET':
        ship_inst = get_object_or_404(Ship, pk=ship_id)
        ship_coordinates = ship_inst.shipcoordinates_set.all()
        return HttpResponse(serialize('json', ship_coordinates))
    else:
        return HttpResponse(status=405)


def get_ship(request, shipd_id):
    """
    """
    return HttpResponse("Place holder, work in progress.")


def get_ship_status(request, ship_id):
    """
    Returns the detail of a ship

    """
    if request.method == 'GET':
        ship_inst = get_object_or_404(Ship, pk=ship_id)
        return JsonResponse(ship_inst, safe=False)
    else:
        return HttpResponse(status=405)
