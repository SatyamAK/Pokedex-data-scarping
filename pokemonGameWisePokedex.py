from bs4 import BeautifulSoup
from requests import get
from re import sub
from json import dump
from pokemonDataExtractor import pokemon_data_extractor

games_list_url = 'https://pokemondb.net/pokedex'

def _games_list_extractor():
    gamesPageHtml = BeautifulSoup(get(games_list_url).text, 'lxml')
    games = [ game.find('a').text.strip() for game in gamesPageHtml.find('nav', class_='panel panel-nav').find_all('ul')[1].find_all('li') ]
    games.pop(0)
    return games

games = _games_list_extractor()

def _game_name_processor(game_name):
    return sub(r'[^a-zA-Z0-9\s]+', '', game_name).lower().replace('  ', ' ').replace(' ', '-')

def _games_url_extractor():
    base_url = games_list_url+'/game'
    games_url = []
    for game in games:
        if(game == 'Black 2 & White 2'):
            game = 'Black & White 2'
        if(game == "Let's Go Pikachu & Let's Go Eevee"):
            game = "Let's Go Pikachu & Eevee"
        game_url = base_url+"/"+_game_name_processor(game)
        games_url.append(game_url)
        
    return games_url

games_url = _games_url_extractor()

def pokemon_game_wise_data_populator():
    for index, game_url in enumerate(games_url):
        dex = {}
        pokemonListPage = BeautifulSoup(get(game_url).text, 'lxml')
        pokemon_data = pokemonListPage.find('div', class_='infocard-list infocard-list-pkmn-lg')
        pokemons = [ pokemon_data_extractor(data) for data in pokemon_data.find_all('span', class_='infocard-lg-data text-muted') ]
        dex['game'] = games[index]
        dex['pokemon'] = pokemons
        file_path = "data/"+_game_name_processor(games[index])+'.json'
        with open(file_path, 'w') as fp:   
            dump(dex, fp)