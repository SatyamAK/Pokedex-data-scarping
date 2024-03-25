from re import split

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