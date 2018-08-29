"""
Controllers for the Battleship application

"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db import DatabaseError, DataError
from django.utils import timezone

from .models import Game, Ship, Tile, Play

# Create your views here.


def games(request):
    """
    """
    if request.method == 'POST':
        game = Game.objects.create(start_date=timezone.now())
        return HttpResponse("Game created: {}".format(game.pk))
    elif request.method == 'GET':
        games_list = Game.objects.all()
        return HttpResponse(games_list[:10])


def get_game(request, game_id):
    """
    """
    if request.method == 'GET':
        game_inst = get_object_or_404(Game, pk=game_id)
        return HttpResponse("Date: {}".format(game_inst.start_date))


def place_ship(request, game_id):
    """
    """
    game_inst = get_object_or_404(Game, pk=game_id)
    if request.method == 'POST':
        orientation = request.POST.get('orientation', Ship.HORIZONTAL)
        ship_type = request.POST.get('type', Ship.CRUISER)
        row = request.POST.get('row', 0)
        column = request.POST.get('column', 0)
        ship_inst = game_inst.ship_set.create(orientation=orientation,
                                              tile_size=ship_type,
                                              is_alive=True)
        ship_inst.tile_set.create(hit=False, row=row, column=column)
        for _ in range(ship_inst.tile_size - 1):
            if ship_inst.orientation == 'HR':
                ship_inst.tile_set.create(hit=False, row=row, column=column)
        return HttpResponse("Ship id: {}".format(ship_inst.pk))
    elif request.method == 'GET':
        ship_list = game_inst.ship_set.all()
        return HttpResponse(ship_list[:10])


def get_ship_detail(request, game_id, ship_id):
    """
    """
    if request.method == 'GET':
        ship_inst = get_object_or_404(Ship, pk=ship_id)
        return HttpResponse("Ship: {}".format(ship_inst.pk))
    else:
        return HttpResponse("Error")


def add_tile(request, ship_id):
    """
    """
    ship_inst = get_object_or_404(Ship, pk=ship_id)
    for i in range(5):
        ship_inst.tile_set.create(hit=False, row=i, column=i+1)
    for tile in ship_inst.tile_set.all():
        print("{0}:{1}".format(tile.pk, tile.hit))
    return HttpResponse("Tile:{}".format(ship_inst.tile_set.all()))


def torpedo(request, game_id):
    """
    """
    if request.method == 'GET':
        row = request.GET.get('row', -1)
        column = request.GET.get('column', -1)
        return HttpResponse('Torpedo fired! row={0}, column={1}'.format(row, column))
