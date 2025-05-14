import os
import sys
from django.core.management import execute_from_command_line

def start_server():
    # Указываем путь к настройкам Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_server.settings')
    
    # Добавляем путь к проекту в PYTHONPATH
    project_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_path)
    
    # Проверяем и применяем миграции
    if not os.path.exists('db.sqlite3'):
        execute_from_command_line(['manage.py', 'makemigrations', 'game'])
        execute_from_command_line(['manage.py', 'migrate'])
    
    # Запускаем сервер
    execute_from_command_line(['manage.py', 'runserver'])

if __name__ == "__main__":
    start_server()

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver