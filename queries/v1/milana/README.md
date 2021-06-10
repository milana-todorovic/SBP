# Upiti

### 1. Za svaku igru odrediti koliko različitih autora je igralo u bar jednom prenosu, i pronaći 3 autora koja su je igrala u najviše prenosa. - 184 sekunda 

```
db.getCollection('streams').aggregate([
    {$group: {_id: {game: "$game.name", broadcaster: "$broadcaster.name"}, streams: {$addToSet: "$stream_id"}}},
    {$project: {game: "$_id.game", broadcaster: {name: "$_id.broadcaster", number_of_streams: {$size: "$streams"}}}},
    {$sort: {"broadcaster.number_of_streams": -1}},
    {$group: {_id: "$game", broadcasters: {$push: "$broadcaster"}}},
    {$project: {_id: 0, game: "$_id", broadcasters: {$slice: ["$broadcasters", 3]}, broadcaster_count: {$size: "$broadcasters"}}},
    {$sort: {"broadcaster_count": -1}}
], {allowDiskUse: true}) 
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v1/milana/1.PNG?raw=true "Rezultat upita")

### 2. Pronaći 5 igara koje su prenošene najveći broj minuta. - 186 sekunda 

```
db.getCollection('streams').aggregate([
    {$group: {_id: {game: "$game.name", stream_id: "$stream_id"}, start: {$min: "$timestamp"}, end: {$max: "$timestamp"}}},
    {$project: {game: "$_id.game", duration_in_minutes: {$divide: [{$subtract: ["$end", "$start"]}, 60000]}}},
    {$group: {_id: "$game", minutes_streamed: {$sum: "$duration_in_minutes"}}},
    {$sort: {"minutes_streamed": -1}},
    {$limit: 5},
    {$project: {_id: 0, game: "$_id", minutes_streamed: "$minutes_streamed"}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v1/milana/2.PNG?raw=true "Rezultat upita")

### 3. Koliki je broj prenosa, i prosjek, minimum, i maksimum prosječnog broja gledalaca po prenosu za svaku igru? - 187 sekunda 

```
db.getCollection('streams').aggregate([
    {$group: {_id: {game: "$game.name", stream_id: "$stream_id"}, average_views: {$avg: "$current_views"}}},
    {$group: {_id: "$_id.game", average_views: {$avg: "$average_views"}, max_views: {$max: "$average_views"}, min_views: {$min: "$average_views"}, count: {$sum: 1}}},
    {$sort: {"average_views": -1}},
    {$project: {_id: 0, game: "$_id", max_views_per_stream: "$max_views", average_views_per_stream: "$average_views", min_views_per_stream: "$min_views", number_of_streams: "$count"}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v1/milana/3.PNG?raw=true "Rezultat upita")

### 4. Za svaki žanr odrediti prosječno i maksimalno trajanje prenosa, i prosječni broj gledalaca po prenosu. - 202 sekunda 

```
db.getCollection('streams').aggregate([
    {$group: {_id: {game: "$game.name", stream_id: "$stream_id", genres: "$game.genres"}, start: {$min: "$timestamp"}, end: {$max: "$timestamp"}, views: {$avg: "$current_views"}}},
    {$project: {genres: "$_id.genres", views: "$views", duration_in_minutes: {$divide: [{$subtract: ["$end", "$start"]}, 60000]}}},
    {$unwind: "$genres"},
    {$group: {_id: "$genres", average_stream_duration: {$avg: "$duration_in_minutes"}, max_stream_duration: {$max: "$duration_in_minutes"}, average_views: {$avg: "$views"}}},
    {$sort: {"average_stream_duration": -1}},
    {$project: {genre: "$genres", average_stream_duration: 1, max_stream_duration: 1, average_views: 1}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v1/milana/4.PNG?raw=true "Rezultat upita")

### 5. Za sve autore koji su najveći broj minuta igrali igru The Evil Within, a pored toga su igrali bar još jednu igru, pronaći koje su još igre igrali, u koliko prenosa, koliko ukupno minuta, i koliko minuta u prosjeku po prenosu. - 197

```
db.getCollection('streams').aggregate([
    {$group: {_id: {game: "$game.name", stream_id: "$stream_id", broadcaster: "$broadcaster.name"}, start: {$min: "$timestamp"}, end: {$max: "$timestamp"}}},
    {$project: {game: "$_id.game", broadcaster: "$_id.broadcaster", duration_in_minutes: {$divide: [{$subtract: ["$end", "$start"]}, 60000]}}},
    {$group: {_id: {game: "$game", broadcaster: "$broadcaster"}, number_of_streams: {$sum: 1}, total_minutes: {$sum: "$duration_in_minutes"}, average_minutes: {$avg: "$duration_in_minutes"}}},
    {$project: {game: "$_id.game", broadcaster: "$_id.broadcaster", number_of_streams: 1, total_minutes: 1, average_minutes: 1}},
    {$sort: {"total_minutes": -1}},
    {$group: {_id: "$broadcaster", games: {$push: {name: "$game", number_of_streams: "$number_of_streams", total_minutes: "$total_minutes", average_minutes: "$average_minutes"}}}},
    {$project: {_id: 0, broadcaster: "$_id", games: 1}},
    {$match: {"games.0.name": "The Evil Within", "games.1": {$exists: true}}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v1/milana/5.PNG?raw=true "Rezultat upita")
