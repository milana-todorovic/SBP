# Upiti

### 1. Za svaku igru odrediti koliko različitih autora je igralo u bar jednom prenosu, i pronaći 3 autora koja su je igrala u najviše prenosa. - 2.44 sekunda sa indeksom, 2.55 sekunda bez indeksa

```
db.getCollection('games-broadcasters').aggregate([
    {$sort: {"number_of_streams": -1}},
    {$group: {_id: "$game.name", broadcasters: {$push: {name: "$broadcaster.name", number_of_streams: "$number_of_streams"}}}},
    {$project: {_id: 0, game: "$_id", broadcasters: {$slice: ["$broadcasters", 3]}, broadcaster_count: {$size: "$broadcasters"}}},
    {$sort: {"broadcaster_count": -1}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v2/milana/1.PNG?raw=true "Rezultat upita")

### 2. Pronaći 5 igara koje su prenošene najveći broj minuta. - 0.899 sekunda 

```
db.getCollection('games-broadcasters').aggregate([
    {$group: {_id: "$game.name", minutes_streamed: {$sum: "$total_duration_in_minutes"}}},
    {$sort: {"minutes_streamed": -1}},
    {$limit: 5},
    {$project: {_id: 0, game: "$_id", minutes_streamed: "$minutes_streamed"}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v2/milana/2.PNG?raw=true "Rezultat upita")

### 3. Koliki je broj prenosa, i prosjek, minimum, i maksimum prosječnog broja gledalaca po prenosu za svaku igru? - 13.2 sekunda 

```
db.getCollection('streams').aggregate([
    {$project: {_id: 0, genres: "$game.genres", views: {$divide: ["$view_sum", "$timestamp_count"]}, duration_in_minutes: 1}},
    {$unwind: "$genres"},
    {$group: {_id: "$genres", average_stream_duration: {$avg: "$duration_in_minutes"}, max_stream_duration: {$max: "$duration_in_minutes"}, average_views: {$avg: "$views"}}},
    {$sort: {"average_stream_duration": -1}},
    {$project: {genre: "$genres", average_stream_duration: 1, max_stream_duration: 1, average_views: 1}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v2/milana/3.PNG?raw=true "Rezultat upita")

### 4. Za svaki žanr odrediti prosječno i maksimalno trajanje prenosa, i prosječni broj gledalaca po prenosu. - 17.4 sekunda 

```
db.getCollection('streams').aggregate([
    {$project: {_id: 0, genres: "$game.genres", views: {$divide: ["$view_sum", "$timestamp_count"]}, duration_in_minutes: 1}},
    {$unwind: "$genres"},
    {$group: {_id: "$genres", average_stream_duration: {$avg: "$duration_in_minutes"}, max_stream_duration: {$max: "$duration_in_minutes"}, average_views: {$avg: "$views"}}},
    {$sort: {"average_stream_duration": -1}},
    {$project: {genre: "$genres", average_stream_duration: 1, max_stream_duration: 1, average_views: 1}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v2/milana/4.PNG?raw=true "Rezultat upita")

### 5. Za sve autore koji su najveći broj minuta igrali igru The Evil Within, a pored toga su igrali bar još jednu igru, pronaći koje su još igre igrali, u koliko prenosa, koliko ukupno minuta, i koliko minuta u prosjeku po prenosu. - 5.27 sekundi sa indeksom

```
db.getCollection('games-broadcasters').aggregate([
    {$sort: {"total_duration_in_minutes": -1}},
    {$group: {_id: "$broadcaster.name", 
              games: {$push: {name: "$game.name", 
                              number_of_streams: "$number_of_streams", 
                              total_minutes: "$total_duration_in_minutes", 
                              average_minutes: {$divide: ["$total_duration_in_minutes", "$number_of_streams"]}}}}},
    {$project: {_id: 0, broadcaster: "$_id", games: 1}},
    {$match: {"games.0.name": "The Evil Within", "games.1": {$exists: true}}}
], {allowDiskUse: true})
```

Rezultat upita:<br>
![Rezulztat upita](https://github.com/milana-todorovic/SBP/blob/main/queries/v2/milana/5.PNG?raw=true "Rezultat upita")
