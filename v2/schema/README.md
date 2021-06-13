# Druga verzija šeme baze podataka

Druga verzija šeme baze podataka sastoji se iz 5 kolekcija: *games*, *streams*, *broadcasters*, *games-per-time*, i *games-broadcasters*.

### Kolekcija *games*

Kolekcija *games* je ostala ista kao u inicijalnoj šemi.

<details>
  <summary>Primjer jednog dokumenta</summary>
  
![Dokument iz games](./games.PNG?raw=true "Dokument iz games")
  
</details>


### Kolekcija *streams*

Kolekcija *streams* dobijena je primjenom šablona baketiranja i proračunavanja na kolekciju *streams* iz inicijalne šeme. Dokumenti inicijalne kolekcije su grupisani po id-ju prenosa i video igri, tako da se jedan dokument nove kolekcije odnosi na sekciju jednog prenosa u toku koje je igrana jedna video igra. Podaci koji su bili specifični za vremenski trenutak (vrijeme posmatranja, trenutni broj gledalaca, trenutni broj pratilaca autora, i slično) grupisani su u listu (atribut *details* u dokumentu). Dodati su atributi dobjieni proračunavanjem koji su često korišteni u upitima, kao što su prvi trenutak posmatranja, zadnji trenutak posmatranja, procjenjeno trajanje sekcije prenosa, minimalni i maksimalni dostignuti broj gledalaca, i slično.

<details>
  <summary>Primjer jednog dokumenta</summary>
  
![Dokument iz streams](./streams.PNG?raw=true "Dokument iz streams")
  
</details>

<details>
  <summary>Upit kojim je kreirana kolekcija</summary>
  
```
db.getCollection('streams').aggregate([
    {$group: {_id: {stream_id: "$stream_id", 
                    game: "$game", 
                    broadcaster: {_id: "$broadcaster.id", name: "$broadcaster.name", created: "$broadcaster.created"}}, 
              details: {$push: {timestamp: "$timestamp", 
                                current_views: "$current_views", 
                                broadcaster_details: {
                                        follower_number: "$broadcaster.follower_number",
                                        total_views: "$broadcaster.total_views"}}},
              start_time: {$min: "$timestamp"}, 
              end_time: {$max: "$timestamp"},
              max_views: {$max: "$current_views"},
              min_views: {$min: "$current_views"},
              view_sum: {$sum: "$current_views"},
              timestamp_count: {$sum: 1}
              }},
    {$project: {_id: {game: "$_id.game.name", stream_id: "$_id.stream_id"},
                game: "$_id.game",
                stream_id: "$_id.stream_id",
                broadcaster: "$_id.broadcaster",
                details: 1,
                start_time: 1,
                end_time: 1,
                duration_in_minutes: {$divide: [{$subtract: ["$end_time", "$start_time"]}, 60000]},
                max_views: 1,
                min_views: 1,
                view_sum: 1,
                timestamp_count: 1}},
    {$out: {db: "sbp-v2", coll: "streams"}}
], {allowDiskUse: true});
```
  
</details>


### Kolekcija *broadcasters*

Kolekcija *broadcasters* je takođe dobijena primjenom baketiranja na inicijalnu kolekciju *streams*, pri čemu su u ovom slučaju dokumenti grupisani po autoru, i izbačeni atributi koji se ne odnose direktno na autora.

<details>
  <summary>Primjer jednog dokumenta</summary>
  
![Dokument iz broadcasters](./broadcasters.PNG?raw=true "Dokument iz broadcasters")
  
</details>

<details>
  <summary>Upit kojim je kreirana kolekcija</summary>
  
```
db.getCollection('streams').aggregate([
    {$sort: {"timestamp": 1}},
    {$group: {_id: {name: "$broadcaster.name", id: "$broadcaster.id", created: "$broadcaster.created"}, 
              details: {$push: {
                        follower_number: "$broadcaster.follower_number",
                        total_views: "$broadcaster.total_views",
                        timestamp: "$timestamp",
                        partner: "$broadcaster.partner"}}
              }},
    {$project: {_id: {id: "$_id.id", name: "$_id.name"}, name: "$_id.name", created: "$_id.created", details: 1}},
    {$out: {db: "sbp-v2", coll: "broadcasters"}}
], {allowDiskUse: true})
```
  
</details>


### Kolekcija *games-per-time*
 
Kolekcija *games-per-time* dobijena je grupisanjem inicijalne kolekcije *streams* po video igri i vremenu, uz proračunavanje podataka o gledanosti i broju prenosa za igru u posmatranom trenutku koji su bili potrebni za upite.

<details>
  <summary>Primjer jednog dokumenta</summary>
  
![Dokument iz games-per-time](./games-and-time.PNG?raw=true "Dokument iz games-per-time")
  
</details>

<details>
  <summary>Upit kojim je kreirana kolekcija</summary>
  
```
db.getCollection('streams').aggregate([
    {$group: {_id: {game: "$game.name", game_id: "$game._id", genres: "$game.genres", timestamp: "$timestamp"}, 
              total_views: {$sum: "$current_views"},
              total_streams: {$sum: 1}}},
    {$project: {_id: {game: "$_id.game", timestamp: "$_id.timestamp"},
                game: {name: "$_id.game", _id: "$_id.game_id", genres: "$_id.genres"},
                timestamp: "$_id.timestamp",
                total_views: 1,
                total_streams: 1}},
    {$out: {db: "sbp-v2", coll: "games-per-time"}}
    ], {allowDiskUse: true});
```
  
</details>




### Kolekcija *games-broadcasters*
 
Kolekcija *games-broadcasters* dobijena je grupisanjem kolekcije *streams* iz druge verzije šeme po autoru i video igri. Proračunati su podaci o broju prenosa koje je autor imao za igru, i ukupnom trajanju svih tih prenosa. Nad atributima *number_of_streams* i *total_duration_in_minutes* dodatno su podignuti indeksi za potrebe upita.

<details>
  <summary>Primjer jednog dokumenta</summary>
  
![Dokument iz games-broadcasters](./games-broadcasters.PNG?raw=true "Dokument iz games-broadcasters")
  
</details>

<details>
  <summary>Upit kojim je kreirana kolekcija</summary>
  
```
db.getCollection('streams').aggregate([
    {$group: {_id: {broadcaster_id: "$broadcaster._id", broadcaster_name: "$broadcaster.name", game: "$game.name", game_id: "$game._id", genres: "$game.genres"}, 
                number_of_streams: {$sum: 1},
                total_duration_in_minutes: {$sum: "$duration_in_minutes"}}},
    {$project: {_id: {game: "$_id.game", broadcaster: "$_id.broadcaster_name"}, 
                game: {name: "$_id.game", _id: "$_id.game_id", genres: "$_id.genres"}, 
                number_of_streams: 1, total_duration_in_minutes: 1,
                broadcaster: {name: "$_id.broadcaster_name", _id: "$_id.broadcaster_id"}}},
    {$out: {db: "sbp-v2", coll: "games-broadcasters"}}
], {allowDiskUse: true});
```
  
</details>
