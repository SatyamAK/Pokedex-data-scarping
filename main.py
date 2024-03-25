from os import mkdir, path
from pokedex import pokedex_populator
from pokemonGameWisePokedex import pokemon_game_wise_data_populator

def main():
    if not path.isdir('data'):
        mkdir('data')
    pokedex_populator()
    pokemon_game_wise_data_populator()

if __name__ == '__main__':
    main()