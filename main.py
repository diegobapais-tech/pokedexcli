#!/usr/bin/python3

from cli_color_print import *
from cli_commands import CLICommand
from pokecache import PokeCache

import requests


MAP_QUERY_SIZE = 20
MAP_OFFSET_POINTER = 0

pokecache = PokeCache()

cli_command = {}

def quit():
    std_command_output("Closing the Pokedex... Goodbye!")
    raise SystemExit

def show_help():
    std_command_output("Welcome to the Pokedex!")
    std_command_output("Usage:\n\n")
    for _, value in cli_command.items():
        std_command_output(value.info())

def map():
    global MAP_OFFSET_POINTER
    global pokecache

    base_url = "https://pokeapi.co/api/v2/location-area/?limit="
    params = {"limit" : MAP_QUERY_SIZE, "offset" : MAP_OFFSET_POINTER}
    area_endpoint = f"{base_url}?limit={MAP_QUERY_SIZE}&offset={MAP_OFFSET_POINTER}"
    response = pokecache.get(area_endpoint)

    if response is None:
        response = requests.get(base_url,params)
        if response.status_code != 200:
            error_command_output(f"Error while requesting map areas!\n\tStatus Code: {response.status_code}\n\tReason: {response.reason}")
            return
        pokecache.add(area_endpoint, response)
    
    data = response.json()

    if data["previous"] is None:
        std_command_output("You are in the first page!\n")
    
    
    pokemon_areas = data["results"]
    for pokemon_area in pokemon_areas:
        MAP_OFFSET_POINTER += 1
        area_output = str(MAP_OFFSET_POINTER) + ". " + pokemon_area["name"]
        success_command_output(area_output)

    area_count = len(pokemon_areas)  
    if area_count != MAP_QUERY_SIZE:
        
        # To avoid empty command outputs
        if area_count == 0:
            MAP_OFFSET_POINTER -= MAP_QUERY_SIZE
            map()
        
        MAP_OFFSET_POINTER -= area_count
        std_command_output("\nYou are in the last page!")

def bmap():
    global MAP_OFFSET_POINTER

    MAP_OFFSET_POINTER -= 2 * MAP_QUERY_SIZE
    MAP_OFFSET_POINTER = max(MAP_OFFSET_POINTER, 0)

    map()
    
    

def setup_commands():
    cli_command["quit"] = CLICommand("quit", "Exit the Pokedex", quit) 
    cli_command["help"] = CLICommand("help", "Displays a help message", show_help)
    cli_command["map"] = CLICommand("map", "Display the next 20 location areas of the Pokemon world!", map)
    cli_command["bmap"] = CLICommand("bmap", "Display the previous 20 location areas of the Pokemon world!", bmap)  


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
            error_command_output("This command does not exist you can use 'help' if you need it!")
        
        print("")

  


if __name__ == "__main__":
    repl()