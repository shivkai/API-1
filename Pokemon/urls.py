from django.urls import path
from . import views
urlpatterns = [
    path('',views.GetPokemon.as_view(),name='pokemons'), 
    path('add',views.AddPokemon.as_view(),name='newpokemon'),
    path('<str:name>/',views.FindPokemon.as_view(),name='pokemon'),
    path('delete/<int:id>/',views.RemovePokemon.as_view(),name='deletepokemon'),
]
