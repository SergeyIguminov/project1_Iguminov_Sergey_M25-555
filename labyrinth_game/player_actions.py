from . import constants, utils


def show_inventory(game_state):
    if game_state['player_inventory'] is None:
        print("Кажется инвентарь пуст")
    else:
        print("В инвентаре есть:", *game_state['player_inventory'])

def get_input(prompt="> "):
    try:
        player_command = input(prompt).strip().lower()
        return player_command
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    current_room = constants.ROOMS[game_state["current_room"]]
    if direction in ['north', 'south', 'east', 'west']:
        if direction in list(current_room["exits"].keys()):
            if current_room["exits"][direction] == "treasure_room":
                if "rusty_key" in game_state["player_inventory"]:
                    print("Вы используете найденный ключ,"+
                          " чтобы открыть путь в комнату сокровищ.")
                    game_state['current_room'] = current_room['exits'][direction]
                    game_state['steps_taken'] += 1
                    utils.describe_current_room(game_state)
                    utils.random_event(game_state)
                else:
                    print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            else:
                game_state['current_room'] = current_room['exits'][direction]
                game_state['steps_taken'] += 1
                utils.describe_current_room(game_state)
                utils.random_event(game_state)
        else:
            print("Нельзя пойти в этом направлении.")
    else:
        print("Неверно указано направление. Попробуйте ещё раз")

def take_item(game_state, item_name):
    if item_name in constants.ROOMS[game_state['current_room']]['items']:
        if item_name == "treasure_chest":
            print("Вы не можете поднять сундук, он слишком тяжелый.")
        else:
            game_state["player_inventory"].append(item_name)
            constants.ROOMS[game_state['current_room']]['items'].remove(item_name)
            print("Вы подняли:", item_name)
    else:
            print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    if item_name in game_state["player_inventory"]:
        match item_name:
            case "torch": 
                print("В комнате стало светлее")
            case "sword": 
                print("Вы взяли в руки меч и стали увереннее")
            case "bronze box": 
                message = "Вы открыли шкатулку"
                if "rusty_key" in game_state["player_inventory"]:
                    message += " Там ничего не оказалось."
                else:
                    message += " Вы получили ржавый ключ (rusty_key)"
            case _: 
                print("Персонаж не знает как этим пользоваться")
    else:
        print("У вас нет такого предмета")