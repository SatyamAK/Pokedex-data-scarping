from bs4 import BeautifulSoup
from requests import get
from re import split
from json import dump

url = 'https://pokemondb.net/pokedex/national'
pageHtml = BeautifulSoup(get(url).text, "lxml")

generations = [ generation.text.strip().replace(' Pokémon', '') for generation in pageHtml.find_all('h2') ]

pokedex = {}

pokemon_data = pageHtml.find_all('div', class_='infocard-list infocard-list-pkmn-lg')

def pokemon_data_extractor(data):
    pokemon = {}
    types = []
    for index, small in enumerate(data.find_all('small')):
        if index == 0:
            pokemon['id'] = small.text.strip()
            continue
        types = split(" . ", small.text.strip())
    pokemon['name'] = data.find('a').text.strip()
    pokemon['types'] = types
    return pokemon

pokemons = []
for pokemons_each_generation in pokemon_data:
    pokemon_data_generation_wise =  [pokemon_data_extractor(data.find('span', class_="infocard-lg-data text-muted")) for data in pokemons_each_generation.find_all('div', class_='infocard')]
    pokemons.append(pokemon_data_generation_wise)

for index, generation in enumerate(generations):
    pokedex[generation] = pokemons[index]

with open('pokedex.json', 'w') as fp:   
    dump(pokedex, fp)