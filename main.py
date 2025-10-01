#!/usr/bin/python3

from pokedexcli.cli_color_print import *
from pokedexcli.cli_commands import CLICommand
from pokedexcli.pokemon import Stats, Types, Pokemon
from pokedexcli.pokecache import PokeCache
from typing import Any, Dict

import random
import requests


# POKEAPI URLs
POKEAPI_AREA_URL = "https://pokeapi.co/api/v2/location-area/"
POKEMON_INFO_URL = "https://pokeapi.co/api/v2/pokemon/"

# Capture probability thresholds
HIGH_EXP_THRESHOLD = 220
MID_EXP_THRESHOLD  = 120

# Capture probabilities
HIGH_EXP_PROB = 0.2
MID_EXP_PROB  = 0.25
LOW_EXP_PROB  = 0.33

# Number of areas printed in each command
MAP_QUERY_SIZE = 20


class PokedexCLI:
    def __init__(self):
        self.offset_pointer = 0
        self.pokecache = PokeCache()
        self.cli_command = {}
        self.captured_pokemon = {}
        self._setup_commands()

    def exit_cli(self, args=None):
        std_command_output("Closing the Pokedex... Goodbye!")
        raise SystemExit

    def show_help(self, args=None):
        std_command_output("Welcome to the Pokedex!")
        std_command_output("Usage:\n\n")
        for _, value in self.cli_command.items():
            std_command_output(value.info())

    def _fetch_from_api(self, url: str) -> Dict[str, Any]:
        response = self.pokecache.get(url)
        if response is None:
            response = requests.get(url)
            if response.status_code != 200:
                error_command_output(
                    f"Error while requesting {url}!\n"
                    f"\tStatus Code: {response.status_code}\n"
                    f"\tReason: {response.reason}"
                )
                return None
            self.pokecache.add(url, response)
        return response.json()
    
    def _require_args(self, args, command_name):
        usage = getattr(self.cli_command.get(command_name),"usage")
        if not args:
            error_command_output(
                f"Error! '{command_name}' command needs an argument to work!\n"
                f"\tUsage: {usage}"
            )
            return False
        return True


    def _get_area_data(self, offset: int) -> Dict[str, Any]:
        url = f"{POKEAPI_AREA_URL}?limit={MAP_QUERY_SIZE}&offset={offset}"
        return self._fetch_from_api(url)

    def _render_area_page(self, data: dict, offset: int) -> bool:
        pokemon_areas = data["results"]
        area_counter = offset
        for pokemon_area in pokemon_areas:
            area_counter += 1
            area_output = f"{area_counter}. {pokemon_area['name']}"
            success_command_output(area_output)

        current_page = int(offset / MAP_QUERY_SIZE + 1)
        total_elements = data["count"]
        total_pages = int(total_elements / MAP_QUERY_SIZE)
        std_command_output(f"Page: {current_page} of {total_pages}")

        if data["next"] is None:
            std_command_output("You are in the last page!")
            return False

        return True

    def list_next_areas(self, args=None):
        data = self._get_area_data(self.offset_pointer)
        if data is None:
            return

        update_offset_pointer = self._render_area_page(data, self.offset_pointer)
        if update_offset_pointer:
            self.offset_pointer += MAP_QUERY_SIZE

    def list_previous_areas(self, args=None):
        self.offset_pointer -= 2 * MAP_QUERY_SIZE
        self.offset_pointer = max(self.offset_pointer, 0)
        self.list_next_areas()

    def _get_pokemon_encounters(self, area_name: str) -> Dict[str, Any]:
        url = f"{POKEAPI_AREA_URL}{area_name}/"
        return self._fetch_from_api(url)

    def _list_pokemon_encounters(self, data: dict):
        for index, pokemon_info in enumerate(data["pokemon_encounters"]):
            success_command_output(f"{index + 1}. {pokemon_info['pokemon']['name']}")

    def explore_area(self, args=None):
        if not self._require_args(args, "explore"):
            return
        
        area_name = args[0]
        data = self._get_pokemon_encounters(area_name)
        
        self._list_pokemon_encounters(data)

    def _get_pokemon_info(self, pokemon_name: str):
        url = f"{POKEMON_INFO_URL}{pokemon_name}/"
        return self._fetch_from_api(url)
    
    def _capture_probability(self, base_exp):
        if base_exp >= HIGH_EXP_THRESHOLD:
            return HIGH_EXP_PROB
        if base_exp >= MID_EXP_THRESHOLD:
            return MID_EXP_PROB
        return LOW_EXP_PROB
    
    def _throw_pokeball_to(self, pokemon_name: str, data: dict):
        std_command_output(f"Throwing a pokeball to {pokemon_name}...")
        
        base_experience = data["base_experience"]
        return random.random() <= self._capture_probability(base_experience)
    
    def _save_pokemon(self, pokemon_name: str, data: dict):
        stats = {}
        raw_response_stats = data["stats"]
        for stat in raw_response_stats:
           stat_name = stat["stat"]["name"]
           stat_value = stat["base_stat"]
           stats[stat_name] = stat_value

        stats_object = Stats(stats.get("hp"), stats.get("attack"),
                            stats.get("defense"), stats.get("special-attack"),
                            stats.get("special-defense"), stats.get("speed"))
        
        types = [None, None]
        raw_response_types = data["types"]
        for index, type in  enumerate(raw_response_types):
            types[index] = type["type"]["name"]
            
        types_object = Types(types[0], types[1])
        
        height = data["height"]
        weight = data["weight"]

        new_pokemon = Pokemon(pokemon_name, height, weight,
                                 stats_object, types_object)
        
        self.captured_pokemon[pokemon_name] = new_pokemon
     
    
    def catch_pokemon(self, args=None):
        if not self._require_args(args, "catch"):
            return
        
        pokemon_name = args[0]
        if self.captured_pokemon.get(pokemon_name):
            success_command_output(f"{pokemon_name} is already captured!")
            return
        
        data = self._get_pokemon_info(pokemon_name)
        if data is None:
            return

        is_captured = self._throw_pokeball_to(pokemon_name, data)

        if not is_captured:
            warning_command_output(f"{pokemon_name} escaped!")
            return
        
        success_command_output(f"{pokemon_name} was caught!")
        success_command_output(f"{pokemon_name} data added to pokedex!")
        self._save_pokemon(pokemon_name, data)

    def inspect_pokemon(self, args=None):
        if not self._require_args(args, "inspect"):
            return
        
        pokemon_name = args[0]
        pokedex_info =  self.captured_pokemon.get(pokemon_name)

        if pokedex_info is None:
            error_command_output("you have not caught that pokemon")
            return
        
        success_command_output(str(pokedex_info))

    def list_caught_pokemon(self, args=None):
        captured_counter = len(self.captured_pokemon)

        if not captured_counter:
            warning_command_output("No captured pokemon")
            return
        
        captured_pokemon = list(self.captured_pokemon.keys())
        for index, pokemon_name in enumerate(captured_pokemon):
            success_command_output(f"{index + 1}. {pokemon_name}")

        success_command_output(f"Total captured pokemon: {captured_counter}")
        
            

    def _setup_commands(self):
        self.cli_command["quit"] = CLICommand("quit", "Exit the Pokedex", self.exit_cli)
        self.cli_command["help"] = CLICommand("help", "Displays a help message", self.show_help)
        self.cli_command["map"] = CLICommand(
            "map", "Display the next 20 location areas of the Pokemon world!", self.list_next_areas
        )
        self.cli_command["bmap"] = CLICommand(
            "bmap", "Display the previous 20 location areas of the Pokemon world!", self.list_previous_areas
        )
        self.cli_command["explore"] = CLICommand(
            "explore <area_name>", "Show all the pokemon the live in a specific area!", self.explore_area
        )
        self.cli_command["catch"] = CLICommand(
            "catch <pokemon_name>", "Throw a pokeball to an specific pokemon and try to catch it!", self.catch_pokemon
        )
        self.cli_command["list"] = CLICommand(
            "list", "List all the captured pokemon!", self.list_caught_pokemon
        )
        self.cli_command["inspect"] = CLICommand(
            "inspect <pokemon_name>", "Look for data of an specific pokemon in the pokedex!", self.inspect_pokemon
        )

    def repl(self):
        while True:
            next_command = std_command_input("Pokedex > ")
            next_command = next_command.strip()
            if not next_command:
                self.exit_cli()
                continue

            parts = next_command.lower().split()
            command_name = parts[0]
            command_args = parts[1:]


            if command_name in self.cli_command:
                self.cli_command[command_name].callback(command_args)
            else:
                error_command_output("Unknown command!\nYou can use 'help' if you need it!")

            print("")


if __name__ == "__main__":
    PokedexCLI().repl()
