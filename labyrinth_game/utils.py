#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input


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
    if 'treasure_key' in game_state['player_inventory'] or 'rusty_key' in game_state['player_inventory']:
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