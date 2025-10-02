# PokedexCLI
PokedexCLI is a command-line tool to fetch pokemon data with caching, this project was made to enlarge my knowleadge of python and learn to use API.

## Table of contents
1. Features
2. Installation
3. Usage 
4. Testing

## Features

The PokedexCLI allows the following commands:

- **quit** — Exit the Pokedex  
- **help** — Displays a help message  
- **map** — Display the next 20 location areas of the Pokémon world  
- **bmap** — Display the previous 20 location areas of the Pokémon world  
- **explore `<area_name>`** — Show all the Pokémon that live in a specific area  
- **catch `<pokemon_name>`** — Throw a Pokéball to a specific Pokémon and try to catch it  
- **list** — List all the captured Pokémon  
- **inspect `<pokemon_name>`** — Look for data of a specific Pokémon in the Pokédex

## How it works

The `PokedexCLI` is built as an interactive REPL (Read-Eval-Print Loop).  
When you run the program, it waits for commands like `map`, `explore`, or `catch`, and executes the corresponding function.

Here’s the main flow:

1. **Command registration**  
   - At startup, the CLI registers all available commands (e.g. `map`, `catch`, `list`, `inspect`) and maps them to their handler methods.

2. **Caching system**  
   - A custom `PokeCache` is used to temporarily store API responses.  
   - This reduces repeated requests to [PokéAPI](https://pokeapi.co/) and speeds up commands.  
   - Expired entries are automatically cleared when new data is added.

3. **Fetching data from PokéAPI**  
   - `map` and `bmap` request paginated lists of areas from PokéAPI.  
   - `explore <area_name>` shows which Pokémon live in a given area.  
   - `inspect <pokemon_name>` retrieves data for a captured Pokémon.

4. **Catching Pokémon**  
   - `catch <pokemon_name>` fetches details for the Pokémon and simulates throwing a Pokéball.  
   - Capture success is based on the Pokémon’s base experience, with different probability thresholds.  
   - Successful captures are stored in the player’s Pokédex.

5. **Managing your Pokédex**  
   - `list` displays all captured Pokémon with a running total.  
   - `inspect` shows detailed stats (HP, Attack, Defense, Speed, Types, Height, Weight) for a captured Pokémon.

6. **User interaction**  
   - The program runs a loop (`repl`) that waits for commands.  
   - If the input matches a known command, the mapped function is executed.  
   - If the input is unknown, an error message is displayed with a suggestion to use `help`.  
   - Typing `quit` exits the program cleanly.

In short: the CLI acts as a local Pokédex that queries PokéAPI, caches results for efficiency, and lets you explore areas, catch Pokémon, and manage your own mini Pokédex collection — all from the terminal. 

## Installation

Clone te repository:

`git clone https://github.com/diegobapais-tech/pokedexcli.git`

Get into the root folder:

`cd pokedexcli`

Install the requirements:

`pip install -r requirements.txt`

## Usage

You can run the PokedexCLI by typing in the root folder: 

`python3 main.py` 

You can also use:

`./main.py`

## Testing

Run from the root folder: 

`python3 -m pytest` 


