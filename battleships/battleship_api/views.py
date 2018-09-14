"""
Controllers for the Battleship application

"""
from django.core.serializers import serialize
from django.db import DatabaseError, DataError
from django.http import (Http404, HttpRequest, HttpResponse,
                         HttpResponseBadRequest, HttpResponseNotAllowed,
                         HttpResponseServerError)
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Game, Ship, ShipCoordinates
from .serializers import (GameSerializer, ShipCoordinatesSerializer,
                          ShipSerializer)

# Django method views and class views below.


class GameList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    API endpoint to retrieve all games, or create a new Game

    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get(self, request, *args, **kwargs):
        """
        API endpoint for GET requests of Game objects

        :return: json array of Game objects with id, is_over, and start_date

        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        API endpoint for POST requests of Game objects

        :return: HTTP_201 if object was created
        :return: HTTP_400 for a bad request

        """
        return self.create(request, *args, **kwargs)


class GameDetail(RetrieveModelMixin,
                 UpdateModelMixin,
                 DestroyModelMixin,
                 GenericAPIView):
    """
    Class used to retrieve, delete, or update a Game object

    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get(self, request, *args, **kwargs):
        """
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        """
        return self.destroy(request, *args, **kwargs)


class ShipList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    Class used to list, and create ship objects

    """
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer

    def get(self, request, *args, **kwargs):
        """
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        """
        return self.create(request, *args, **kwargs)


class ShipDetails(RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin, GenericAPIView):
    """
    Class used to retrieve, update, or destroy a Ship object

    """
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer

    def get(self, request, *args, **kwargs):
        """
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        """
        return self.destroy(request, *args, **kwargs)

@api_view(['GET'])
def get_alive_ships(request, game_id):
    """
    Returns the ships still in the game

    """
    game_inst = get_object_or_404(Game, pk=game_id)
    ships_left = game_inst.ship_set.filter(is_alive=True)
    serializer = ShipSerializer(ships_left, many=True)
    return Response(serializer.data)
    # return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


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


def get_ship_status(request, ship_id):
    """
    Returns the detail of a ship

    """
    if request.method == 'GET':
        ship_inst = get_object_or_404(Ship, pk=ship_id)
        return JsonResponse(ship_inst, safe=False)
    else:
        return HttpResponse(status=405)
