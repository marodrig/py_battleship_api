"""
Serializers for the battleship REST API

"""
from rest_framework import serializers
from .models import Game, Ship, ShipCoordinates


class GameSerializer(serializers.ModelSerializer):
    """
    Serializer for the Game Model

    """
    class Meta:
        model = Game
        fields = (
            'id',
            'is_over',
            'start_date')


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
        unique_together = ('game', 'orientation')


class ShipCoordinatesSerializer(serializers.ModelSerializer):
    """
    Serializer for the ShipCoordinates Model

    """
    class Meta:
        model = ShipCoordinates
        fields = (
            'id',
            'ship',
            'game',
            'hit',
            'row',
            'column')
