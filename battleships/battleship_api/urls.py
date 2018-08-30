from django.urls import path

from . import views

urlpatterns = [
    path('games/', views.games, name='games'),
    path('games/<int:game_id>/', views.get_game, name='get_game'),
    path('games/<int:game_id>/ships', views.place_ship, name='place_ship'),
    path('games/<int:game_id>/ships/<int:ship_id>/', views.get_ship_detail, 
         name='get_ship_detail'),
    path('games/<int:game_id>/shot', views.torpedo, name='torpedo'),
]
