# Adventure Game (Interactive Fiction)

A text-based adventure game in the interactive fiction genre. Explore a mysterious labyrinth, solve puzzles, collect items, and find the treasure!
---
### Installation (via Poetry — recommended)
- **poetry install**
- **poetry run start**

### Game Objective
Find the treasure! To do this, you will need to collect keys, which can be obtained by: solving riddles in rooms, exploring items, discovering hidden places

### Key Items Required to Win
- **treasure_key** — obtained by solving the riddle in the Hall
- **rusty_key** — found inside the bronze box
- **golden_key** — hidden inside the shiny gem

---
Текстовая приключенческая игра в жанре interactive fiction. Исследуйте таинственный лабиринт, решайте загадки, собирайте предметы и найдите сокровище!
## Установка через Poetry (рекомендуется)
**poetry install**
**poetry run start**

## Цель игры
Найдите сокровище! Для этого вам понадобятся ключи, которые можно получить:
- Решая загадки в комнатах
- Исследуя предметы
- Находя скрытые места

## Ключевые предметы для победы:
- **treasure_key** - за решение загадки в зале
- **rusty_key** - внутри бронзовой шкатулки  
- **golden_key** - внутри блестящего самоцвета

## Полное прохождение
## START
Вы в начале лабиринта. Темные стены нависают над вами.
Заметные предметы: torch
Выходы: north, east
`take torch`
Вы подняли: `torch`
`go north`
Вы пошли на север...
первая загадка и ключ

## HALL 
Просторный зал с высоким потолком. В центре пьедестал.
Заметные предметы: `bronze_box`
Выходы: `south`, `east`, `west`
Кажется, здесь есть загадка (используйте команду solve).
`solve`
Что идет в гору и с горы, но остается на месте?
Ваш ответ: дорога
Правильно! Загадка решена!
Сундук на пьедестале открывается! Вы получаете `treasure_key`!
Библиотека - второй ключ
`go east`
Вы пошли на восток

## LIBRARY
Старая библиотека. Книги покрыты пылью.
Заметные предметы: `ancient_scroll`
Выходы: `west`, `north`
`take ancient_scroll`
В свитке вы находите `rusty_key`!
`go west`

## GARDEN
Заброшенный сад. Фонтан в центре еще работает.
Заметные предметы: `shiny_gem`
Выходы: `east`, `north`
`take shiny_gem`
Фонтан открывает потайное отделение! Вы получаете `golden_key`!

## ARMORY
Оружейная комната. Доспехи стоят как будто живые.
Заметные предметы: `sword`
Выходы: `south`, `east`
`go east`
Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.

## TREASURE_ROOM
КОМНАТА СОКРОВИЩ! Большой сундук стоит в центре.
Заметные предметы: `treasure_chest`
Выходы: `west`
`use treasure_chest`
Вы применяете ключ, и замок щёлкает. Сундук открыт!
В сундуке сокровище! Вы победили!

## Опасности и стратегии
Комната `trap_room` содержит опасную загадку. Неправильный ответ активирует ловушку!
- Без инвентаря: 30% шанс проигрыша
- С предметами: потеря случайного предмета

## Случайные события
При перемещении есть 10% шанс случайного события:
- Находка монетки
- Странные звуки (меч защищает)
- Внезапная ловушка (факел защищает)

**Лицензия**
Учебный проект, созданный в рамках курса по программированию.
