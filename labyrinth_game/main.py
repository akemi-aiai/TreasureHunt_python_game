#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS, COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    clear_screen,
    describe_current_room,
    print_welcome_message,
    show_help,
    solve_puzzle,
)

# Состояние игры
game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0
}


def process_command(game_state, command):
    """Обработка команд пользователя"""
    # Разделяем команду на части
    parts = command.split()
    if not parts:
        return
    
    # Извлекаем основную команду
    main_command = parts[0]
    
    # Обрабатываем команды с помощью match/case
    match main_command:
        case 'look':
            describe_current_room(game_state)
        
        case 'go' if len(parts) > 1:
            direction = parts[1]
            if move_player(game_state, direction):
                describe_current_room(game_state)
        
        # Односложные команды движения
        case 'north' | 'south' | 'east' | 'west' | 'up' | 'down':
            if move_player(game_state, main_command):
                describe_current_room(game_state)
        
        case 'take' if len(parts) > 1:
            item_name = parts[1]
            take_item(game_state, item_name)
        
        case 'use' if len(parts) > 1:
            item_name = parts[1]
            use_item(game_state, item_name)
        
        case 'solve':
            # В treasure_room команда solve открывает сундук
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        
        case 'inventory':
            show_inventory(game_state)
        
        case 'help':
            show_help(COMMANDS)
        
        case 'quit' | 'exit':
            print("Спасибо за игру! До свидания!")
            game_state['game_over'] = True
        
        case _:
            print(f"Неизвестная команда: '{command}'")
            print("Введите 'help' для списка команд.")


def main():
    """Основной игровой цикл"""
    # Очищаем экран и показываем приветствие
    clear_screen()
    print("Добро пожаловать в Лабиринт сокровищ!")
    print_welcome_message()
    
    # Описываем стартовую комнату
    describe_current_room(game_state)
    
    # Основной игровой цикл
    while not game_state['game_over']:
        # Получаем команду от пользователя
        command = get_input("\nВведите команду: ")
        
        # Обрабатываем команду
        process_command(game_state, command)
    
    # Показываем статистику после завершения игры
    print(f"\nИгра завершена! Вы сделали {game_state['steps_taken']} шагов.")


if __name__ == "__main__":
    main()