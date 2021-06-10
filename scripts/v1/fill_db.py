from games import GameParser
from streams import StreamParser
import csv

if __name__ == '__main__':
    print("Games!")
    game_parser = GameParser('steam games/steam.csv')
    game_parser.add_games_to_db(url = 'mongodb://localhost:27017/', db_name = 'sbp-v1')

    print("Streams!")
    stream_parser = StreamParser('twitch')
    stream_parser.add_games_to_db(url = 'mongodb://localhost:27017/', db_name = 'sbp-v1', games = game_parser.get_games())
