from django.urls import path

from . import views

urlpatterns = [
    path('/v1/games/',
         views.get_games_collection,
         name='get_games_collection'),
    path('/v1/games/<int:game_id>/',
         views.get_game_status,
         name='get_game_status'),
    # path('/v1/games/<int:game_id>/ships',
    #      views.place_ship,
    #      name='place_ship'),
    # path('/v1/games/<int:game_id>/ships/<int:ship_id>/',
    #      views.get_ship_detail,
    #      name='get_ship_detail'),
    # path('/v1/games/<int:game_id>/shot',
    #      views.torpedo,
    #      name='torpedo'),
    # path('/v1/games/<int:game_id>/ships/<int:ship_id>/tiles',
    #      views.get_tiles,
    #      name='get_tiles'),
]
