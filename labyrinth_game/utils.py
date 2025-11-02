from . import constants


def describe_current_room(game_state):
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
    puzzle = constants.ROOMS[game_state["current_room"]]["puzzle"]
    if puzzle is None:
        print("Загадок здесь нет")
    else:
        print(puzzle[0])
        answer = input("Ваш ответ: ")
        if answer == puzzle[1]:
            print("Вы справились с этим испытанием!")
            constants.ROOMS[game_state["current_room"]]["puzzle"] = None
            if constants.ROOMS[game_state["current_room"]]["reward"] is not None:
                game_state["player_inventory"].append(constants.ROOMS[game_state["current_room"]]["reward"])
        else:
            print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
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
                    if current_room["puzzle"] == None:
                        print("Сундук открыт!")
                        print("В сундуке сокровище! Вы победили!")
                        game_state["game_over"]=True
            else:
                print("Вы отступаете от сундука.")

def pseudo_random(seed, modulo):
    from math import floor, sin
    spread_result = sin(seed*12.9898)*43758.5453
    fractor_part = spread_result - floor(spread_result)
    return floor(fractor_part*modulo)

def trigger_trap(game_state):
    print("Ловушка активирована! С потолка летит град из стрел!")
    inventar = game_state["player_inventar"]
    if len(inventar) > 0:
        item_index = pseudo_random(game_state["steps_taken"], len(inventar))
        print("О нет, из рюкзака выпал предмет: ", inventar[item_index])
        game_state["player_inventar"].remove[item_index]
    else:
        print("Стрела попала по вам!")
        if pseudo_random(game_state["steps_taken"], 9) < 3:
            print("К сожалению, вы не уцелели. Игра окончена")
        else:
            print("Но вы уцелели!")

def random_event(game_state):
    if pseudo_random(game_state["steps_taken"], 10) == 0:
        match pseudo_random(game_state["steps_taken"], 2):
            case 0: 
                print("Находка! Вы нашли монету (coin)!")
                game_state["player_inventory"].append("coin")
            case 1:
                print("Из темноты доносится шорох.")
                if "sword" in game_state["player_inventory"]:
                    print("Кем бы оно ни было, вы его отпугнули мечом")
            case 2:
                trap_check = game_state["current_room"] == "trap_room"
                torch_check = not( "torch" in game_state["player_inventory"])
                if trap_check and torch_check:
                    print("Ловушка!")
                    trigger_trap(game_state)