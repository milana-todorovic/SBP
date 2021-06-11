# Upiti

### 1. Pronaći 10 igrica koje su imale najviše gledalaca u jednom trenutku (u okviru svih prenosa koji su u tom trenutku bili aktivni). - 2.96 sekunda 

```
db.getCollection('games-per-time').aggregate([
    {$group: {_id: "$_id.game", max_views: {$max: "$total_views"}}},
    {$sort: {"max_views": -1}},
    {$limit: 10},
    {$project: {_id: 0, game: "$_id", max_views: 1}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v2/ana/1.PNG?raw=true "Rezultat upita")

### 2. Za svakog autora odrediti koju je igru igrao najveći broj minuta. - 4.56 sekunda sa indeksom, ~8 sekundi bez indeksa

```
db.getCollection('games-broadcasters').aggregate([
    {$sort: {"total_duration_in_minutes": -1}},
    {$group: {_id: "$broadcaster.name", games: {$push: {name: "$game.name", total_minutes: "$total_duration_in_minutes"}}}},
    {$project: {_id: 0, broadcaster: "$_id", most_played_game: {$arrayElemAt: [ "$games", 0 ]}}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v2/ana/2.PNG?raw=true "Rezultat upita")

### 3. Za svaki sat u danu pronaći koja je igra imala u prosjeku najviše prenosa.- 5.38 sekunda 

```
db.getCollection('games-per-time').aggregate([
    {$project: {game: "$game.name", hour: {$hour: "$timestamp"}, stream_count: "$total_streams"}},
    {$group: {_id: {game: "$game", hour: "$hour"}, average_stream_count: {$avg: "$stream_count"}}},    
    {$project: {game: "$_id.game", hour: "$_id.hour", average_stream_count: 1}},
    {$sort: {"average_stream_count": -1}},
    {$group: {_id: "$hour", games: {$push: {name: "$game", average_stream_count: "$average_stream_count"}}}},
    {$project: {_id: 0, hour: "$_id", most_played_game: {$arrayElemAt: [ "$games", 0 ]}}},    
    {$sort: {"hour": 1}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v2/ana/3.PNG?raw=true "Rezultat upita")

### 4. Koje igre je prenosio autor koji je ostvario najveći rast broja pratilaca u posmatranom vremenskom periodu? - 4.86 sekunda 

```
db.getCollection('broadcasters').aggregate([
    {$project: {_id: 0, broadcaster: "$name", start_details: {$arrayElemAt: [ "$details", 0 ]}, end_details: {$arrayElemAt: [ "$details", -1 ]}}},
    {$project: {broadcaster: 1, follower_change: {$subtract: ["$end_details.follower_number", "$start_details.follower_number"]}}},
    {$sort: {"follower_change": -1}},
    {$limit: 1},
    {$lookup:
     {
       from: "games-broadcasters",
       localField: "broadcaster",
       foreignField: "_id.broadcaster",
       as: "games"
     }},
     {$project: {broadcaster: 1, follower_change: 1, games: "$games.game.name"}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v2/ana/4.PNG?raw=true "Rezultat upita")

### 5. Koje žanrove je prenosio najveći broj autora? - 2.99 sekunda 

```
db.getCollection('games-broadcasters').aggregate([
    {$project: {genres: "$game.genres", broadcaster: "$broadcaster.name"}},
    {$unwind: "$genres"},
    {$group: {_id: "$genres", broadcasters: {$addToSet: "$broadcaster"}}},
    {$project: {genre: "$genres", broadcasters: 1, broadcaster_count: {$size: "$broadcasters"}}},
    {$sort: {"broadcaster_count": -1}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v2/ana/5.PNG?raw=true "Rezultat upita")
