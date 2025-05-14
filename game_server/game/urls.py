from django.urls import path
from . import views

app_name: str = 'game'

urlpatterns = [
    path('api/state/', views.game_state),
]