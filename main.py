#!/usr/bin/python3

from cli_color_print import *
from cli_commands import CLICommand
from pokecache import PokeCache

import requests

POKEAPI_AREA_URL = "https://pokeapi.co/api/v2/location-area/"
MAP_QUERY_SIZE = 20
MAP_OFFSET_POINTER = 0

pokecache = PokeCache()

cli_command = {}

def exit_cli():
    std_command_output("Closing the Pokedex... Goodbye!")
    raise SystemExit

def show_help():
    std_command_output("Welcome to the Pokedex!")
    std_command_output("Usage:\n\n")
    for _, value in cli_command.items():
        std_command_output(value.info())

def _build_area_endpoint(offset: int) -> str:
    return f"{POKEAPI_AREA_URL}?limit={MAP_QUERY_SIZE}&offset={offset}"

def _get_area_data(offset: int):
    area_enpoint = _build_area_endpoint(offset)
    response = pokecache.get(area_enpoint)

    if response is None:
        params = {"limit" : MAP_QUERY_SIZE, "offset" : offset}
        response = requests.get(POKEAPI_AREA_URL,params)
        if response.status_code != 200:
            error_command_output(f"Error while requesting map areas!\n"
                                 f"\tStatus Code: {response.status_code}\n"
                                 f"\tReason: {response.reason}")
            return

        pokecache.add(area_enpoint, response)

    return response.json()

def _render_area_page(data: dict, offset: int) -> bool:

    pokemon_areas = data["results"]
    area_counter = offset
    for pokemon_area in pokemon_areas:
        area_counter += 1
        area_output = str(area_counter) + ". " + pokemon_area["name"]
        success_command_output(area_output)

    current_page = offset // MAP_QUERY_SIZE + 1
    std_command_output(f"Current page: {current_page}")

    if data["next"] is None:
        std_command_output("You are in the last page!")
        return False
    
    return True


def list_next_areas():
    global MAP_OFFSET_POINTER
    global pokecache

    data = _get_area_data(MAP_OFFSET_POINTER)
    if data is None:
        return

    update_offset_pointer = _render_area_page(data, MAP_OFFSET_POINTER)
    if update_offset_pointer:
        MAP_OFFSET_POINTER += MAP_QUERY_SIZE


def list_previous_areas():
    global MAP_OFFSET_POINTER

    MAP_OFFSET_POINTER -= 2 * MAP_QUERY_SIZE
    MAP_OFFSET_POINTER = max(MAP_OFFSET_POINTER, 0)

    list_next_areas()
    
    

def setup_commands():
    cli_command["quit"] = CLICommand("quit", "Exit the Pokedex", exit_cli) 
    cli_command["help"] = CLICommand("help", "Displays a help message", show_help)
    cli_command["map"] = CLICommand("map", "Display the next 20 location areas of the Pokemon world!", list_next_areas)
    cli_command["bmap"] = CLICommand("bmap", "Display the previous 20 location areas of the Pokemon world!", list_previous_areas)  


def repl():
    setup_commands()

    while True:
        next_command = std_command_input("Pokedex > ")
        next_command = next_command.strip()
        if not next_command:
            quit()
            continue

        parts = next_command.split()
        next_command = parts[0]
        next_command = next_command.lower()

        if next_command in cli_command:
            cli_command[next_command].callback()
        else:
            error_command_output("Unknown command!\nYou can use 'help' if you need it!")
        
        print("")

  


if __name__ == "__main__":
    repl()