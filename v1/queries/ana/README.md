# Upiti

### 1. Pronaći 10 igrica koje su imale najviše gledalaca u jednom trenutku (u okviru svih prenosa koji su u tom trenutku bili aktivni). - 162 sekunda 

```
db.getCollection('streams').aggregate([
    {$group: {_id: {game: "$game.name", timestamp: "$timestamp"}, total_views: {$sum: "$current_views"}}},
    {$group: {_id: "$_id.game", max_views: {$max: "$total_views"}}},
    {$sort: {"max_views": -1}},
    {$limit: 10},
    {$project: {_id: 0, game: "$_id", max_views: 1}}
], {allowDiskUse: true}) 
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v1/ana/1.PNG?raw=true "Rezultat upita")

### 2. Za svakog autora odrediti koju je igru igrao najveći broj minuta. - 198 sekunda 

```
db.getCollection('streams').aggregate([
    {$group: {_id: {game: "$game.name", stream_id: "$stream_id", broadcaster: "$broadcaster.name"}, start: {$min: "$timestamp"}, end: {$max: "$timestamp"}}},
    {$project: {game: "$_id.game", broadcaster: "$_id.broadcaster", duration_in_minutes: {$divide: [{$subtract: ["$end", "$start"]}, 60000]}}},
    {$group: {_id: {game: "$game", broadcaster: "$broadcaster"}, total_minutes: {$sum: "$duration_in_minutes"}}},
    {$project: {game: "$_id.game", broadcaster: "$_id.broadcaster", total_minutes: 1}},
    {$sort: {"total_minutes": -1}},
    {$group: {_id: "$broadcaster", games: {$push: {name: "$game", total_minutes: "$total_minutes"}}}},
    {$project: {_id: 0, broadcaster: "$_id", most_played_game: {$arrayElemAt: [ "$games", 0 ]}}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v1/ana/2.PNG?raw=true "Rezultat upita")

### 3. Za svaki sat u danu pronaći koja je igra imala u prosjeku najviše prenosa.- 151 sekunda 

```
db.getCollection('streams').aggregate([
    {$group: {_id: {game: "$game.name", timestamp: "$timestamp"}, stream_count: {$sum: 1}}},
    {$project: {game: "$_id.game", hour: {$hour: "$_id.timestamp"}, stream_count: 1}},
    {$group: {_id: {game: "$game", hour: "$hour"}, average_stream_count: {$avg: "$stream_count"}}},    
    {$project: {game: "$_id.game", hour: "$_id.hour", average_stream_count: 1}},
    {$sort: {"average_stream_count": -1}},
    {$group: {_id: "$hour", games: {$push: {name: "$game", average_stream_count: "$average_stream_count"}}}},
    {$project: {_id: 0, hour: "$_id", most_played_game: {$arrayElemAt: [ "$games", 0 ]}}},    
    {$sort: {"hour": 1}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v1/ana/3.PNG?raw=true "Rezultat upita")

### 4. Koje igre je prenosio autor koji je ostvario najveći rast broja pratilaca u posmatranom vremenskom periodu? - 463 sekunda 

```
db.getCollection('streams').aggregate([
    {$sort: {"timestamp": 1}},
    {$group: {_id: "$broadcaster.name", follower_counts: {$push: "$broadcaster.follower_number"}, played_games: {$addToSet: "$game.name"}}},
    {$project: {_id: 0, broadcaster: "$_id", played_games: 1, start_follower_count: {$arrayElemAt: [ "$follower_counts", 0 ]}, end_follower_count: {$arrayElemAt: [ "$follower_counts", -1 ]}}},
    {$project: {broadcaster: 1, played_games: 1, follower_change: {$subtract: ["$end_follower_count", "$start_follower_count"]}}},
    {$sort: {"follower_change": -1}},
    {$limit: 1}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v1/ana/4.PNG?raw=true "Rezultat upita")

### 5. Koje žanrove je prenosio najveći broj autora? - 186 sekunda 

```
db.getCollection('streams').aggregate([
    {$project: {genres: "$game.genres", broadcaster: "$broadcaster.name"}},
    {$unwind: "$genres"},
    {$group: {_id: "$genres", broadcasters: {$addToSet: "$broadcaster"}}},
    {$project: {genre: "$genres", broadcasters: 1, broadcaster_count: {$size: "$broadcasters"}}},
    {$sort: {"broadcaster_count": -1}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v1/ana/5.PNG?raw=true "Rezultat upita")
