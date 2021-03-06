"""
Controllers for the Battleship application

"""
import json

from django.core.serializers import serialize
from django.db import DatabaseError, DataError
from django.http import (Http404, HttpRequest, HttpResponse,
                         HttpResponseBadRequest, HttpResponseNotAllowed,
                         HttpResponseServerError, QueryDict)
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response

from .models import Game, Ship, ShipCoordinate
from .serializers import (GameSerializer, ShipCoordinateSerializer,
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


def get_game_coordinates(request, game_id):
    """
    """
    if request.method == 'GET':
        game_inst = get_object_or_404(Game, pk=game_id)
        game_coordinates = game_inst.shipcoordinates_set.all()
        return HttpResponse(serialize('json', game_coordinates))
    return HttpResponse(status=405)


@api_view(['GET', 'POST'])
def get_post_game_ships(request, game_id):
    """
    """
    game_inst = get_object_or_404(Game, pk=game_id)
    if request.method == 'POST':
        game_inst.rand_init_ships()
        ships_created = game_inst.ship_set.all().count()
        data = {
            'ships_created': ships_created,
        }
        return Response(data=data)
    if request.method == 'GET':
        game_ships = game_inst.ship_set.all()
        serializer = ShipSerializer(game_ships, many=True)
        return Response(serializer.data)


@api_view(['PUT'])
def put_play(request, game_id):
    """
    """
    data = {}
    put_req = QueryDict(request.body)
    print(put_req)
    row_from_req = put_req.get('row', -1)
    col_from_req = put_req.get('column', -1)
    game_inst = get_object_or_404(Game, pk=game_id)
    try:
        coord_inst = game_inst.shipcoordinate_set.get(
            ship_row=row_from_req,
            ship_col=col_from_req)
        coord_inst.hit = True
        coord_inst.save()
        data['hit'] = coord_inst.hit
    except ShipCoordinate.DoesNotExist:
        data['hit'] = False
    return Response(data=data)


@api_view(['GET'])
def get_ship_coordinates(request, ship_id):
    """
    """
    ship_inst = get_object_or_404(Ship, pk=ship_id)
    ship_coordinates = ship_inst.shipcoordinate_set.all()
    serializer = ShipCoordinateSerializer(ship_coordinates, many=True)
    return Response(serializer.data)
