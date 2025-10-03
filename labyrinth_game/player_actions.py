#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS


def get_input(prompt="> "):
    """Получить ввод от пользователя с обработкой ошибок"""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def look_around(room, rooms):
    """Описание текущей комнаты"""
    print(f"\n{room['description']}")
    
    if room['exits']:
        exits = ', '.join(room['exits'].keys())
        print(f"Выходы: {exits}")
    
    if room['items']:
        items = ', '.join(room['items'])
        print(f"Предметы в комнате: {items}")
    
    if room['puzzle']:
        print("Здесь есть загадка! Используйте команду 'solve', "
              "чтобы попытаться её решить.")


def move_player(game_state, direction):
    """Перемещение игрока между комнатами"""
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    # Проверяем, существует ли выход в этом направлении
    if direction in current_room['exits']:
        # Получаем название новой комнаты
        new_room_name = current_room['exits'][direction]
        
        # Обновляем текущую комнату
        game_state['current_room'] = new_room_name
        
        # Увеличиваем счетчик шагов
        game_state['steps_taken'] += 1
        
        # Выводим сообщение о перемещении
        print(f"Вы пошли на {direction}.")
        
        # Возвращаем успешное выполнение
        return True
    else:
        # Выводим сообщение об ошибке
        print("Нельзя пойти в этом направлении.")
        return False


def take_item(game_state, item_name):
    """Взять предмет из комнаты"""
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    # Проверяем, есть ли предмет в комнате
    if item_name in current_room['items']:
        # Добавляем предмет в инвентарь игрока
        game_state['player_inventory'].append(item_name)
        
        # Удаляем предмет из списка предметов комнаты
        current_room['items'].remove(item_name)
        
        # Выводим сообщение о успешном взятии
        print(f"Вы подняли: {item_name}")
        return True
    else:
        # Выводим сообщение об ошибке
        print("Такого предмета здесь нет.")
        return False


def use_item(game_state, item_name):
    """Использовать предмет из инвентаря"""
    # Проверяем, есть ли предмет у игрока
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return False
    
    # Обрабатываем разные предметы
    match item_name:
        case 'torch':
            print("Вы зажигаете факел. Вокруг стало светлее!")
            return True
        
        case 'sword':
            print("Вы достаете меч. Чувствуете себя увереннее с оружием в руках!")
            return True
        
        case 'bronze box':
            print("Вы открываете бронзовую шкатулку...")
            if 'rusty key' not in game_state['player_inventory']:
                game_state['player_inventory'].append('rusty key')
                print("Внутри вы находите rusty key!")
            else:
                print("Шкатулка пуста.")
            return True
        
        case 'treasure chest':
            # Проверяем, находимся ли мы в комнате с сокровищами
            from labyrinth_game.utils import attempt_open_treasure
            if game_state['current_room'] == 'treasure_room':
                return attempt_open_treasure(game_state)
            else:
                print("Здесь нет подходящего места для сундука.")
            return False
        
        case _:
            print(f"Вы не знаете, как использовать {item_name}.")
            return False


def show_inventory(game_state):
    """Показать инвентарь игрока"""
    inventory = game_state['player_inventory']
    
    if inventory:
        items_list = ', '.join(inventory)
        print(f"\nВаш инвентарь: {items_list}")
    else:
        print("\nВаш инвентарь пуст.")#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS


def get_input(prompt="> "):
    """Получить ввод от пользователя с обработкой ошибок"""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def look_around(room, rooms):
    """Описание текущей комнаты"""
    print(f"\n{room['description']}")
    
    if room['exits']:
        exits = ', '.join(room['exits'].keys())
        print(f"Выходы: {exits}")
    
    if room['items']:
        items = ', '.join(room['items'])
        print(f"Предметы в комнате: {items}")
    
    if room['puzzle']:
        print("Здесь есть загадка! Используйте команду 'solve', "
              "чтобы попытаться её решить.")


def move_player(game_state, direction):
    """Перемещение игрока между комнатами"""
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    # Проверяем, существует ли выход в этом направлении
    if direction in current_room['exits']:
        # Получаем название новой комнаты
        new_room_name = current_room['exits'][direction]
        
        # Обновляем текущую комнату
        game_state['current_room'] = new_room_name
        
        # Увеличиваем счетчик шагов
        game_state['steps_taken'] += 1
        
        # Выводим сообщение о перемещении
        print(f"Вы пошли на {direction}.")
        
        # Возвращаем успешное выполнение
        return True
    else:
        # Выводим сообщение об ошибке
        print("Нельзя пойти в этом направлении.")
        return False


def take_item(game_state, item_name):
    """Взять предмет из комнаты"""
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    # Проверяем, есть ли предмет в комнате
    if item_name in current_room['items']:
        # Добавляем предмет в инвентарь игрока
        game_state['player_inventory'].append(item_name)
        
        # Удаляем предмет из списка предметов комнаты
        current_room['items'].remove(item_name)
        
        # Выводим сообщение о успешном взятии
        print(f"Вы подняли: {item_name}")
        return True
    else:
        # Выводим сообщение об ошибке
        print("Такого предмета здесь нет.")
        return False


def use_item(game_state, item_name):
    """Использовать предмет из инвентаря"""
    # Проверяем, есть ли предмет у игрока
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return False
    
    # Обрабатываем разные предметы
    match item_name:
        case 'torch':
            print("Вы зажигаете факел. Вокруг стало светлее!")
            return True
        
        case 'sword':
            print("Вы достаете меч. Чувствуете себя увереннее с оружием в руках!")
            return True
        
        case 'bronze box':
            print("Вы открываете бронзовую шкатулку...")
            if 'rusty key' not in game_state['player_inventory']:
                game_state['player_inventory'].append('rusty key')
                print("Внутри вы находите rusty key!")
            else:
                print("Шкатулка пуста.")
            return True
        
        case 'treasure chest':
            # Проверяем, находимся ли мы в комнате с сокровищами
            from labyrinth_game.utils import attempt_open_treasure
            if game_state['current_room'] == 'treasure_room':
                return attempt_open_treasure(game_state)
            else:
                print("Здесь нет подходящего места для сундука.")
            return False
        
        case _:
            print(f"Вы не знаете, как использовать {item_name}.")
            return False


def show_inventory(game_state):
    """Показать инвентарь игрока"""
    inventory = game_state['player_inventory']
    
    if inventory:
        items_list = ', '.join(inventory)
        print(f"\nВаш инвентарь: {items_list}")
    else:
        print("\nВаш инвентарь пуст.")