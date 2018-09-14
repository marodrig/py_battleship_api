from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('games/',
         views.GameList.as_view(),
         name='game-list'),
    path('games/<int:game_id>/play',
         views.put_play,
         name='put_play'),
    path('games/<int:pk>/',
         views.GameDetail.as_view(),
         name='game-details'),
    path('games/<int:game_id>/aliveShips',
         views.get_alive_ships,
         name='get_alive_ships'),
    path('games/<int:game_id>/coordinates',
         views.get_game_coordinates,
         name='get_game_coordinates'),
    path('games/<int:game_id>/ships',
         views.get_post_game_ships,
         name='get_post_game_ships'),
    path('ships/',
         views.ShipList.as_view(),
         name='ship-list'),
    path('ships/<int:pk>/',
         views.ShipDetails.as_view(),
         name='ship-details'),
    path('ships/<int:ship_id>/coordinates',
         views.get_ship_coordinates,
         name='get_ship_coordinates'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
