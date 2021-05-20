"""
Serializers for the battleship REST API

"""
from rest_framework import serializers
from .models import Game, Ship, ShipCoordinate


class ShipSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ship Model

    """

    class Meta:
        model = Ship
        fields = (
            'id',
            'game',
            'orientation',
            'length',
            'is_alive')


class GameSerializer(serializers.ModelSerializer):
    """
    Serializer for the Game Model

    """
    ships = ShipSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = (
            'id',
            'is_over',
            'start_date',
            'ships')


class ShipCoordinateSerializer(serializers.ModelSerializer):
    """
    Serializer for the ShipCoordinates Model

    """
    class Meta:
        model = ShipCoordinate
        fields = (
            'id',
            'ship',
            'game',
            'hit',
            'ship_row',
            'ship_col')
