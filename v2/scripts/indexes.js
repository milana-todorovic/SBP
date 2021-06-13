db.getCollection('games-broadcasters').createIndex({"total_duration_in_minutes": -1})

db.getCollection('games-broadcasters').createIndex({"number_of_streams": -1})