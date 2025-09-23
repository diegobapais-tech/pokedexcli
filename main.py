#!/usr/bin/python3

from cli_color_print import *
from cli_commands import CLICommand
from typing import Any, Dict
from pokecache import PokeCache
import requests

# TODO: probably wrap this into config file
POKEAPI_AREA_URL = "https://pokeapi.co/api/v2/location-area/"
MAP_QUERY_SIZE = 20


class PokedexCLI:
    def __init__(self):
        self.offset_pointer = 0
        self.pokecache = PokeCache()
        self.cli_command = {}
        self._setup_commands()

    def exit_cli(self, args=None):
        std_command_output("Closing the Pokedex... Goodbye!")
        raise SystemExit

    def show_help(self, args=None):
        std_command_output("Welcome to the Pokedex!")
        std_command_output("Usage:\n\n")
        for _, value in self.cli_command.items():
            std_command_output(value.info())

    def _build_area_endpoint(self, offset: int) -> str:
        return f"{POKEAPI_AREA_URL}?limit={MAP_QUERY_SIZE}&offset={offset}"

    def _get_area_data(self, offset: int) -> Dict[str, Any]:
        area_endpoint = self._build_area_endpoint(offset)
        response = self.pokecache.get(area_endpoint)

        if response is None:
            params = {"limit": MAP_QUERY_SIZE, "offset": offset}
            response = requests.get(POKEAPI_AREA_URL, params)
            if response.status_code != 200:
                error_command_output(
                    f"Error while requesting map areas!\n"
                    f"\tStatus Code: {response.status_code}\n"
                    f"\tReason: {response.reason}"
                )
                return None

            self.pokecache.add(area_endpoint, response)

        return response.json()

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

        


if __name__ == "__main__":
    PokedexCLI().repl()
