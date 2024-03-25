from bs4 import BeautifulSoup
from requests import get
from re import sub
from json import dump
import pokedex

games_list_url = 'https://pokemondb.net/pokedex'
gamePageHtml = BeautifulSoup(get(games_list_url).text, 'lxml')
games = [ game.find('a').text.strip() for game in gamePageHtml.find('nav', class_='panel panel-nav').find_all('ul')[1].find_all('li') ]

base_url = games_list_url+'/game'
games_url = []
for game in games:
    if(game == 'National Dex'):
        continue
    if(game == 'Black 2 & White 2'):
        game = 'Black & White 2'
    if(game == "Let's Go Pikachu & Let's Go Eevee"):
        game = "Let's Go Pikachu & Eevee"

    game_url = base_url+"/"+sub(r'[^a-zA-Z0-9\s]+', '', game).lower().replace('  ', ' ').replace(' ', '-')
    games_url.append(game_url)