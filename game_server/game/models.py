from django.db import models

class GameState(models.Model):
    player_x = models.IntegerField(default=500)
    player_y = models.IntegerField(default=500)
    enemies = models.JSONField(default=list)  # [{"x": 200, "y": 300}]
    last_updated = models.DateTimeField(auto_now=True)