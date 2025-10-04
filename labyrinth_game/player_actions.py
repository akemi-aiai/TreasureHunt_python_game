#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import get_input, pseudo_random


def random_event(game_state):
    """
    Случайные события, которые происходят во время перемещения игрока
    
    Args:
        game_state (dict): состояние игры
    
    Returns:
        bool: True если событие произошло, False если нет
    """
    steps = game_state['steps_taken']
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    # С вероятностью 10% происходит случайное событие
    if pseudo_random(steps, 10) == 0:
        event_type = pseudo_random(steps, 3)  # 3 типа событий
        
        if event_type == 0:
            # Сценарий 1: Находка
            print("\n Что-то блеснуло на полу...")
            if 'coin' not in current_room['items']:
                current_room['items'].append('coin')
                print("Вы нашли монетку! Она добавлена в комнату.")
            else:
                print("Вы видите монетку, но она уже была здесь.")
            return True
        
        elif event_type == 1:
            # Сценарий 2: Испуг
            print("\n Вы слышите странный шорох в темноте...")
            if 'sword' in game_state['player_inventory']:
                print("Вы достаете меч, и шорох сразу прекращается!")
            else:
                print("Вам становится не по себе... Лучше поторопиться!")
            return True
        
        elif event_type == 2:
            # Сценарий 3: Срабатывание ловушки
            if (current_room_name == 'trap_room' and 
                'torch' not in game_state['player_inventory']):
                print("\n В темноте вы не заметили скрытую ловушку!")
                return trigger_trap(game_state)
            else:
                # Если условия не выполнены, происходит обычное событие
                print("\n Вам повезло! Вы нашли небольшой самоцвет.")
                if 'small gem' not in game_state['player_inventory']:
                    game_state['player_inventory'].append('small gem')
                    print("Вы получаете small gem!")
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
        
        print(f"Из вашего инвентаря выпал: {lost_item}")
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
    
    print(f"\n{question}")
    
    user_answer = get_input("Ваш ответ: ")
    
    # Создаем список альтернативных ответов
    alternative_answers = {
        '10': ['десять', 'ten'],
        'резонанс': ['огонь', 'fire'],
        'шаг шаг шаг': ['step step step', 'steps'],
        'имя': ['name'],
        'время': ['time', 'час', 'clock']
    }
    
    # Проверяем ответ (основной или альтернативный)
    is_correct = (
        user_answer.lower() == correct_answer.lower() or
        user_answer.lower() in alternative_answers.get(correct_answer, [])
    )
    
    if is_correct:
        print("Загадка решена!")
        
        # Убираем загадку из комнаты
        room['puzzle'] = None
        
        # Добавляем награду в зависимости от комнаты
        if current_room_name == 'hall':
            print("Сундук на пьедестале открывается! Вы получаете treasure_key!")
            game_state['player_inventory'].append('treasure_key')
        elif current_room_name == 'library':
            print("В свитке вы находите rusty_key!")
            game_state['player_inventory'].append('rusty_key')
        elif current_room_name == 'garden':
            print("Фонтан открывает потайное отделение! Вы получаете golden_key!")
            game_state['player_inventory'].append('golden_key')
        elif current_room_name == 'treasure_room':
            print("Замок на двери щелкает! Теперь вы можете открыть сундук.")
        else:
            print("Вы стали ближе к разгадке!")
        
        return True
    else:
        print("Неверно. Попробуйте снова.")
        
        # В trap_room неверный ответ активирует ловушку
        if current_room_name == 'trap_room':
            print("Ой,неправильный ответ активирует защитный механизм!")
            return trigger_trap(game_state)
        
        return False


def attempt_open_treasure(game_state):
    """Попытка открыть сундук с сокровищами"""
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    
    if 'treasure chest' not in room['items']:
        print("Сундук уже открыт или отсутствует.")
        return False
    
    has_treasure_key = 'treasure_key' in game_state['player_inventory']
    has_rusty_key = 'rusty_key' in game_state['player_inventory']
    
    if has_treasure_key or has_rusty_key:
        print("Вы используете ключ, и замок щёлкает. Сундук открыт!")
        
        room['items'].remove('treasure chest')
        
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return True
    
    # Если ключей нет, предлагаем ввести код
    print("Сундук заперт. У вас нет подходящего ключа.")
    choice = get_input("Ввести код? (да/нет): ")
    
    if choice.lower() in ['да', 'yes', 'y']:
        if room['puzzle']:
            _, correct_code = room['puzzle']
            user_code = get_input("Введите код: ")
            
            if user_code == correct_code:
                print("Код принят! Сундук открывается!")
                
                room['items'].remove('treasure chest')

                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
                return True
            else:
                print("Неверный код.")
                return False
        else:
            print("Нет возможности ввести код.")
            return False
    else:
        print("Вы отступаете от сундука.")
        return False


def move_player(game_state, direction):
    """Перемещение игрока между комнатами"""
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    # Проверяем, существует ли выход в этом направлении
    if direction in current_room['exits']:
        # Получаем название новой комнаты
        new_room_name = current_room['exits'][direction]
        
        # Проверяем специальные условия для treasure_room
        if new_room_name == 'treasure_room':
            # Проверяем наличие ключей для доступа в комнату сокровищ
            has_treasure_key = 'treasure_key' in game_state['player_inventory']
            has_rusty_key = 'rusty_key' in game_state['player_inventory']
            has_golden_key = 'golden_key' in game_state['player_inventory']
            
            if has_treasure_key or has_rusty_key or has_golden_key:
                print("Вы используете найденный ключ, чтобы открыть")
                print("путь в комнату сокровищ.")
                # Продолжаем перемещение
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return False
        
        # Обновляем текущую комнату
        game_state['current_room'] = new_room_name
        
        # Увеличиваем счетчик шагов
        game_state['steps_taken'] += 1
        
        # Выводим сообщение о перемещении
        print(f"Вы пошли на {direction}.")
        
        # Проверяем случайное событие
        random_event(game_state)
        
        return True
    else:
        # Выводим сообщение об ошибке
        print("Тут нельзя пройти!")
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
            print("Вы достаете меч.")
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
            if game_state['current_room'] == 'treasure_room':
                return attempt_open_treasure(game_state)
            else:
                print("Здесь нет сундука.")
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