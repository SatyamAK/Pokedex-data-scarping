from bs4 import BeautifulSoup
from requests import get
from re import sub
from json import dump
from pokemonDataExtractor import pokemon_data_extractor

games_list_url = 'https://pokemondb.net/pokedex'
gamesPageHtml = BeautifulSoup(get(games_list_url).text, 'lxml')
games = [ game.find('a').text.strip() for game in gamesPageHtml.find('nav', class_='panel panel-nav').find_all('ul')[1].find_all('li') ]
games.pop(0)

base_url = games_list_url+'/game'
games_url = []

def game_name_processor(game_name):
    return sub(r'[^a-zA-Z0-9\s]+', '', game_name).lower().replace('  ', ' ').replace(' ', '-')

for game in games:
    if(game == 'Black 2 & White 2'):
        game = 'Black & White 2'
    if(game == "Let's Go Pikachu & Let's Go Eevee"):
        game = "Let's Go Pikachu & Eevee"

    game_url = base_url+"/"+game_name_processor(game)
    games_url.append(game_url)

for index, game_url in enumerate(games_url):
    dex = {}
    pokemonListPage = BeautifulSoup(get(game_url).text, 'lxml')
    pokemon_data = pokemonListPage.find('div', class_='infocard-list infocard-list-pkmn-lg')
    pokemons = [ pokemon_data_extractor(data) for data in pokemon_data.find_all('span', class_='infocard-lg-data text-muted') ]
    dex['game'] = games[index]
    dex['pokemon'] = pokemons
    with open(game_name_processor(games[index]), 'w') as fp:   
        dump(dex, fp)