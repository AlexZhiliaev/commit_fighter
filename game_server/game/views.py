from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import GameState

@api_view(['GET', 'POST'])
def game_state(request):
    # Создаем состояние с врагами по умолчанию
    state, created = GameState.objects.get_or_create(
        id=1,
        defaults={
            'player_x': 400,
            'player_y': 300,
            'enemies': [  # Добавляем 2 врага по умолчанию
                {"x": 200, "y": 200},
                {"x": 600, "y": 400}
            ]
        }
    )
    
    # Если враги почему-то пустые, инициализируем их
    if not state.enemies:
        state.enemies = [
            {"x": 200, "y": 200},
            {"x": 600, "y": 400}
        ]
        state.save()
    
    if request.method == 'POST':
        state.player_x = request.data.get('x', state.player_x)
        state.player_y = request.data.get('y', state.player_y)
        state.save()
    
    return Response({
        'player': {'x': state.player_x, 'y': state.player_y},
        'enemies': state.enemies
    })