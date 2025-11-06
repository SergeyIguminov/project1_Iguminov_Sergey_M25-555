from . import constants


def describe_current_room(game_state):
    """
    Функция описания текущей комнаты

    Аргументы: состояние игры (из main.py). 

    Возвращает: описание комнаты из файла constants.py, а также видимые в комнате предметы и есть ли загадки в комнате. 
    """
    current_room = constants.ROOMS[game_state["current_room"]]
    print("==" + game_state["current_room"] + "==")
    print(current_room["description"])
    if len(current_room["items"]) > 0:
        print("Видимые предметы:", *current_room["items"])
    exits = ", ".join(current_room["exits"].keys())
    print(f"Выходы: {exits}")
    if current_room["puzzle"] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    """
    Функция решения пазла
    Аргументы: состояние игры (из main.py)
    Выводит загадку хронящуюся в constants.py и запрашивает у игрока ответ.
    При верном ответе выдаёт награду.
    """
    puzzle = constants.ROOMS[game_state["current_room"]]["puzzle"]
    if puzzle is None:
        print("Загадок здесь нет")
    else:
        print(puzzle[0])
        answer = input("Ваш ответ: ")
        if answer in puzzle[1]:
            print("Вы справились с этим испытанием!")
            constants.ROOMS[game_state["current_room"]]["puzzle"] = None
            if constants.ROOMS[game_state["current_room"]]["reward"] is not None:
                game_state["player_inventory"].append(constants.ROOMS[game_state["current_room"]]["reward"])
        else:
            if game_state["current_room"] == "trap_room":
                trigger_trap(game_state)
            print("Неверно. Попробуйте снова.")

def show_help():
    """
    Функция справки
    Выводит на экран команды доступные игроку
    """
    for key in list(constants.COMMANDS.keys()):
                print(key, constants.COMMANDS[key], sep=" - ")

def attempt_open_treasure(game_state):
    """
    Функция попытки открыть сокровище (финал игры)
    Проверяет условие чтобы игровой персонаж имел ключ от сундука и находился в treasure room.
    Также может как альтернативу предложить решение загадки. 
    При успешном открытии - уведомляет о выйгрыше и заканчивает игру.
    """
    current_room = constants.ROOMS[game_state["current_room"]]
    if game_state["current_room"] == "treasure_room":
        if "treasure_key" in game_state["player_inventory"]:
            print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
            print("В сундуке сокровище! Вы победили!")
            current_room["items"].remove("treasure_chest")
            game_state["game_over"]=True


        else:
            print("Сундук заперт. Ввести код? (да/нет)")
            if input("> ") == "да":
                if current_room["puzzle"] is not None:
                    solve_puzzle(game_state)
                    if current_room["puzzle"] is None:
                        print("Сундук открыт!")
                        print("В сундуке сокровище! Вы победили!")
                        game_state["game_over"]=True
            else:
                print("Вы отступаете от сундука.")

def pseudo_random(seed, modulo):
    """
    Функция вызова случайны чисел. 
    Использует формулу синуса с большими числами.

    Аргументы: seed - любое число. modulo - предел максимального числа, которое может сгенерироваться.

    Возвращает: Целое число (int)
    """
    from math import floor, sin
    spread_result = sin(seed*12.9898)*43758.5453
    fractor_part = spread_result - floor(spread_result)
    return floor(fractor_part*modulo)

def trigger_trap(game_state):
    """
    Функция активации ловушки
    Реализуют логику выпадения вещей из инвентаря если он там есть, либо нанесение урона игроку.
    Внутри себя использует функцию pseudo_random

    Аргемунты: состояние игры из main.py
    """
    print("Ловушка активирована! С потолка летит град из стрел!")
    inventory = game_state["player_inventory"].copy()
    if len(inventory) > 0:
        item_index = pseudo_random(game_state["steps_taken"], len(inventory)-1)
        print("О нет, из рюкзака выпал предмет: ", inventory[item_index])
        game_state["player_inventory"].remove(inventory[item_index])
    else:
        print("Стрела попала по вам!")
        MODUL_OF_RANDOM = 9
        CHANCE_OF_GAME_OVER = 3
        if pseudo_random(game_state["steps_taken"], MODUL_OF_RANDOM) < CHANCE_OF_GAME_OVER:
            print("К сожалению, вы не уцелели. Игра окончена")
        else:
            print("Но вы уцелели!")

def random_event(game_state):
    """
    Функция  случайных событий при переходе между локациями. 
    Вызывает одно из 3 случайных событий.

    Аргументы: состояние игры из main.py
    """
    MODUL_OF_RANDOM = 10
    CHANCE_OF_RANDOM_EVENT = 0
    if pseudo_random(game_state["steps_taken"], MODUL_OF_RANDOM) == CHANCE_OF_RANDOM_EVENT:
        NUMBER_OF_RANDOM_EVENT = 2
        match pseudo_random(game_state["steps_taken"], NUMBER_OF_RANDOM_EVENT):
            case 0: 
                print("Находка! Вы нашли монету (coin)!")
                game_state["player_inventory"].append("coin")
            case 1:
                print("Из темноты доносится шорох.")
                if "sword" in game_state["player_inventory"]:
                    print("Кем бы оно ни было, вы его отпугнули мечом")
            case 2:
                trap_check = game_state["current_room"] == "trap_room"
                torch_check =  "torch" not in game_state["player_inventory"]
                if trap_check and torch_check:
                    print("Ловушка!")
                    trigger_trap(game_state)