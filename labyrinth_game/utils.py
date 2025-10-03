#!/usr/bin/env python3

import math

from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input


def pseudo_random(seed, modulo):
    """
    Генератор псевдослучайных чисел на основе синуса
    
    Args:
        seed (int): начальное значение (например, количество шагов)
        modulo (int): верхняя граница диапазона [0, modulo)
    
    Returns:
        int: случайное число в диапазоне [0, modulo)
    """
    # Используем формулу на основе синуса для генерации псевдослучайного числа
    x = math.sin(seed * 12.9898) * 43758.5453
    
    # Получаем дробную часть
    fractional_part = x - math.floor(x)
    
    # Приводим к нужному диапазону и возвращаем целое число
    return int(fractional_part * modulo)


def random_event(game_state):
    """
    Случайное событие, которое может произойти при перемещении
    
    Args:
        game_state (dict): состояние игры
    
    Returns:
        bool: True если событие произошло, False если нет
    """
    steps = game_state['steps_taken']
    
    # С вероятностью 20% происходит случайное событие
    if pseudo_random(steps, 100) < 20:
        event_type = pseudo_random(steps, 3)  # 3 типа событий
        
        if event_type == 0:
            print("\n💫 Вы нашли случайный предмет на полу!")
            if 'healing herb' not in game_state['player_inventory']:
                game_state['player_inventory'].append('healing herb')
                print("Вы получили healing herb!")
            return True
        
        elif event_type == 1:
            print("\n Вас охватило странное чувство дежавю...")
            print("Кажется, вы уже были здесь раньше.")
            return True
        
        elif event_type == 2:
            print("\n💎 Блеск в углу привлек ваше внимание!")
            if 'small gem' not in game_state['player_inventory']:
                game_state['player_inventory'].append('small gem')
                print("Вы нашли small gem!")
            return True
    
    return False

def trigger_trap(game_state):
    """
    Активация ловушки с негативными последствиями для игрока
    
    Args:
        game_state (dict): состояние игры
    
    Returns:
        bool: True если игра окончена, False если игрок выжил
    """
    print("\n Ловушка активирована! Пол стал дрожать...")
    
    # Проверяем инвентарь игрока
    inventory = game_state['player_inventory']
    
    if inventory:
        # Если есть предметы, теряем случайный предмет
        item_count = len(inventory)
        lost_item_index = pseudo_random(game_state['steps_taken'], item_count)
        lost_item = inventory[lost_item_index]
        
        # Удаляем предмет из инвентаря
        inventory.pop(lost_item_index)
        
        print(f"Из вашего инвентаря выпал и потерялся: {lost_item}")
        print("К счастью, вы остались живы!")
        return False
    
    else:
        # Если инвентарь пуст, игрок получает "урон"
        print("У вас нет предметов для защиты!")
        damage_chance = pseudo_random(game_state['steps_taken'], 10)
        
        if damage_chance < 3:  # 30% шанс проигрыша
            print("Вас настигает ловушка! Вы не успели увернуться...")
            print("Игра окончена!")
            game_state['game_over'] = True
            return True
        else:
            print("Вам чудом удалось увернуться от ловушки!")
            return False


def clear_screen():
    """Очистить экран (кроссплатформенный способ)"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_welcome_message():
    """Вывести приветственное сообщение"""
    print("=" * 50)
    print("          ЛАБИРИНТ ТАЙН")
    print("=" * 50)
    print("Добро пожаловать в загадочный лабиринт!")
    print("Используйте команды: go, look, take, inventory, solve, quit")
    print("Направления: north, south, east, west")
    print("=" * 50)


def format_direction(direction):
    """Форматировать направление для красивого вывода"""
    direction_names = {
        'north': 'север',
        'south': 'юг', 
        'east': 'восток',
        'west': 'запад',
        'up': 'вверх',
        'down': 'вниз'
    }
    return direction_names.get(direction, direction)


def describe_current_room(game_state):
    """Описание текущей комнаты"""
    # Получаем данные о текущей комнате
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    
    # Выводим название комнаты в верхнем регистре
    print(f"\n== {current_room_name.upper()} ==")
    
    # Выводим описание комнаты
    print(f"{room['description']}")
    
    # Выводим заметные предметы, если они есть
    if room['items']:
        items_list = ', '.join(room['items'])
        print(f"Заметные предметы: {items_list}")
    
    # Выводим доступные выходы
    if room['exits']:
        exits_list = ', '.join(room['exits'].keys())
        print(f"Выходы: {exits_list}")
    
    # Сообщение о наличии загадки
    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Решение загадки в текущей комнате"""
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    
    # Проверяем, есть ли загадка в комнате
    if not room['puzzle']:
        print("Загадок здесь нет.")
        return
    
    # Получаем вопрос и правильный ответ
    question, correct_answer = room['puzzle']
    
    # Выводим вопрос
    print(f"\n{question}")
    
    # Получаем ответ от пользователя
    user_answer = get_input("Ваш ответ: ")
    
    # Сравниваем ответы
    if user_answer.lower() == correct_answer.lower():
        print("Правильно! Загадка решена!")
        
        # Убираем загадку из комнаты
        room['puzzle'] = None
        
        # Добавляем награду
        if current_room_name == 'treasure_room':
            print("Вы получаете treasure_key!")
            game_state['player_inventory'].append('treasure_key')
        elif current_room_name == 'hall':
            print("Сундук на пьедестале открывается! Вы получаете ancient_key!")
            game_state['player_inventory'].append('ancient_key')
        
        return True
    else:
        print("Неверно. Попробуйте снова.")
        return False


def attempt_open_treasure(game_state):
    """Попытка открыть сундук с сокровищами"""
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    
    # Проверяем наличие сундука
    if 'treasure chest' not in room['items']:
        print("Сундук уже открыт или отсутствует.")
        return False
    
    # Проверяем наличие ключей
    has_treasure_key = 'treasure_key' in game_state['player_inventory']
    has_rusty_key = 'rusty_key' in game_state['player_inventory']
    
    if has_treasure_key or has_rusty_key:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        
        # Удаляем сундук из комнаты
        room['items'].remove('treasure chest')
        
        # Объявляем победу
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return True
    
    # Если ключей нет, предлагаем ввести код
    print("Сундук заперт. У вас нет подходящего ключа.")
    choice = get_input("Ввести код? (да/нет): ")
    
    if choice.lower() in ['да', 'yes', 'y']:
        # Проверяем, есть ли загадка в комнате
        if room['puzzle']:
            _, correct_code = room['puzzle']
            user_code = get_input("Введите код: ")
            
            if user_code == correct_code:
                print("Код принят! Сундук открывается!")
                
                # Удаляем сундук из комнаты
                room['items'].remove('treasure chest')
                
                # Объявляем победу
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
                return True
            else:
                print("Неверный код. Сундук остается запертым.")
                return False
        else:
            print("Нет возможности ввести код.")
            return False
    else:
        print("Вы отступаете от сундука.")
        return False


def show_help():
    """Показать справку по командам игры"""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")