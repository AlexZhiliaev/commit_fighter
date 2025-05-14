import pygame
import requests
import threading
import time

SERVER_URL = "http://localhost:8000/api/state/"

class GameClient:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player_pos = [400, 300]
        self.enemies = []
        self.running = True
        self.last_update = 0
        self.network_thread = None
        
        # Начальная загрузка данных
        self.update_game_state()

    def update_game_state(self):
        try:
            response = requests.get(SERVER_URL, timeout=0.5)
            data = response.json()
            self.enemies = data['enemies']
        except Exception as e:
            print(f"Ошибка обновления: {e}")

    def send_player_position(self):
        try:
            requests.post(SERVER_URL, 
                        json={'x': self.player_pos[0], 'y': self.player_pos[1]},
                        timeout=0.5)
        except:
            pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        keys = pygame.key.get_pressed()
        speed = 5
        
        # Локальное движение без ожидания сервера
        if keys[pygame.K_LEFT]: self.player_pos[0] -= speed
        if keys[pygame.K_RIGHT]: self.player_pos[0] += speed
        if keys[pygame.K_UP]: self.player_pos[1] -= speed
        if keys[pygame.K_DOWN]: self.player_pos[1] += speed
        
        # Отправка обновления в отдельном потоке
        if any(keys):
            if self.network_thread is None or not self.network_thread.is_alive():
                self.network_thread = threading.Thread(target=self.send_player_position)
                self.network_thread.start()

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Враги
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, (255, 0, 0),
                           (enemy['x']-15, enemy['y']-15, 30, 30))
        
        # Игрок
        pygame.draw.rect(self.screen, (0, 255, 0),
                       (self.player_pos[0]-20, self.player_pos[1]-20, 40, 40))
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            
            # Обновление данных с сервера (10 раз в секунду)
            current_time = time.time()
            if current_time - self.last_update > 0.1:
                if self.network_thread is None or not self.network_thread.is_alive():
                    self.network_thread = threading.Thread(target=self.update_game_state)
                    self.network_thread.start()
                self.last_update = current_time
            
            self.draw()
            self.clock.tick(60)  # 60 FPS

if __name__ == "__main__":
    client = GameClient()
    client.run()
    pygame.quit()