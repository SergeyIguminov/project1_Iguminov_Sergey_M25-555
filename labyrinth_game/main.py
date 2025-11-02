#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from . import player_actions, utils

game_state = {
    "player_inventory": [],  # Инвентарь игрока
    "current_room": "entrance",  # Текущая комната
    "game_over": False,  # Значения окончания игры
    "steps_taken": 0,  # Количество шагов
}


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    utils.describe_current_room(game_state)

    while not game_state["game_over"]:
        process_command(game_state, player_actions.get_input())
        


def process_command(game_state, command):
    command_name = command.split()[0]
    if len(command.split()) > 1:
        command_attribute = command.split()[1]
    match command_name:
        case "look":
            utils.describe_current_room(game_state)
        case "use":
            player_actions.use_item(game_state, command_attribute)
        case "go":
            player_actions.move_player(game_state, command_attribute)
        case "take":
            player_actions.take_item(game_state, command_attribute)
        case "inventory":
            if len(game_state["player_inventory"]) > 0:
                print("В инвентаре есть:", *game_state["player_inventory"])
            else:
                print("В инвентаре пока ничего нет")
        case "solve":
            if game_state["current_room"]=="treasure_room":
                utils.attempt_open_treasure(game_state)
            else:
                utils.solve_puzzle(game_state)
        case "quit":
            game_state["game_over"] = True


if __name__ == "__main__":
    main()
