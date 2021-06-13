from dateutil import parser
import pymongo
import csv

class GameParser:
    def __init__(self, file):
        self._file = file

    def add_games_to_db(self, url, db_name):
        client = pymongo.MongoClient(url)
        db = client[db_name]
        games = []
        self._games = {}
        with open(self._file, 'r', encoding = 'cp850') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                game = get_game(row)
                games.append(game)
                self._games[game['name']] = get_mini_game(game)

        db['games'].insert_many(games)

    def get_games(self):
        return self._games


def get_game(row) -> dict:
    eng = False
    if (row['english'] == 1):
        eng = True

    return {
        '_id': row['appid'],
        'name': row['name'],
        'release_date': parser.parse(row['release_date']),
        'english': eng,
        'developer': row['developer'],
        'publisher': row['publisher'],
        'platforms': row['platforms'].split(';'),
        'required_age': int(row['required_age']),
        'categories': row['categories'].split(';'),        
        'genres': row['genres'].split(';'),        
        'steamspy_tags': row['steamspy_tags'].split(';'),
        'achievements': int(row['achievements']),
        'positive_ratings': int(row['positive_ratings']),
        'negative_ratings': int(row['negative_ratings']),
        'average_playtime': int(row['average_playtime']),
        'median_playtime': int(row['median_playtime']),
        'owners': row['owners'],
        'price': float(row['price'])
    }

def get_mini_game(game) -> dict:
    return {
        '_id': game['_id'],
        'name': game['name'],
        'release_date': game['release_date'],
        'publisher': game['publisher'],
        'categories': game['categories'],        
        'genres': game['genres'],
        'price': game['price']
    }
