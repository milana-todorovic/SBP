import datetime
from dateutil import parser
import pymongo
import csv
import os

class StreamParser:
    def __init__(self, dir):
        self._dir = dir

    def add_games_to_db(self, url, db_name, games):
        client = pymongo.MongoClient(url)
        db = client[db_name]

        for file in os.listdir(self._dir):
            print('\t' + file)
            timestamp = get_datetime(file)
            streams = []
            with open(os.path.join(self._dir, file), 'r', encoding = 'cp850') as csv_file:
                reader = csv.DictReader(csv_file, fieldnames=['stream_id', 'current_views', 'start_time', 'game', 'broadcaster_id', 'broadcaster_name', 'delay_setting', 'follower_number', 'partner', 'broadcaster_language', 'total_views', 'language', 'broadcaster_created', 'bitrate', 'resolution'], delimiter='\t')
                for row in reader:
                    if row['game'] in games:
                        try:
                            streams.append(get_stream(timestamp, row, games[row['game']]))
                        except:
                            print("Bad row")
            
            if (len(streams) > 0):
                db['streams'].insert_many(streams)


def get_stream(timestamp, row, game):
    partner = True
    if (row['partner'] == '-1'):
        partner = False

    broadcaster = {
        'id': row['broadcaster_id'],
        'name': row['broadcaster_name'],
        'follower_number': int(row['follower_number']),
        'partner': partner,
        'language': row['broadcaster_language'],
        'total_views': int(row['total_views']),
        'created': parser.parse(row['broadcaster_created'])
    }

    if broadcaster['follower_number'] == -1:
        broadcaster['follower_number'] = 0
    if broadcaster['total_views'] == -1:
        broadcaster['total_views'] = 0

    return {
        'timestamp': timestamp,
        'stream_id': int(row['stream_id']),
        'current_views': int(row['current_views']),
        'start_time': parser.parse(row['start_time']),
        'game': game,
        'language': row['language'],
        'broadcaster': broadcaster
    }

def get_datetime(filename) -> datetime:
    split1 = filename.split('.')
    split2 = split1[0].split('-')
    year = int(split2[1])
    month = int(split2[2])
    day = int(split2[3])
    hour = int(split2[4])
    minute = int(split2[5])
    return datetime.datetime(year, month, day, hour, minute)