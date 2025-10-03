#!/usr/bin/env python3

import math
import os


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


def clear_screen():
    """Очистить экран (кроссплатформенный способ)"""
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


def show_help(commands):
    """Показать справку по командам игры"""
    print("\nДоступные команды:")
    for command, description in commands.items():
        # Форматируем вывод: команда занимает 16 символов слева
        print(f"  {command:<16} - {description}")


def get_input(prompt="> "):
    """Получить ввод от пользователя с обработкой ошибок"""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"