from django.urls import path

from . import views

urlpatterns = [
    path('games/',
         views.get_post_games,
         name='get_post_games'),
    path('games/<int:game_id>/',
         views.get_delete_patch_game,
         name='get_delete_patch_game'),
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
         views.get_post_ships,
         name='get_post_ships'),
    path('ships/<int:ship_id>',
         views.get_ship,
         name='get_ship'),
    path('ships/<int:ship_id>/coordinates',
         views.get_ship_coordinates,
         name='get_ship_coordinates'),
]
