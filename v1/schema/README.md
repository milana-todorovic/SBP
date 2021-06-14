# Prva verzija šeme baze podataka

Prva verzija šeme baze podataka prati strukturu skupa podata, i sastoji se iz dvije kolekcije: *games* i *streams*.

### Kolekcija *games*

Svaki dokument u kolekciji *games* predstavlja zapis o jednoj video igri, i odgovara jednom redu datoteke *steam.csv* iz [skupa podataka sa Steam-a](https://www.kaggle.com/nikdavis/steam-store-games). 

Primjer jednog dokumenta: <br> ![Dokument iz games](./games.PNG?raw=true "Dokument iz games")

### Kolekcija *streams*

Svaki dokument u kolekciji *streams* odgovara jednom redu iz datoteka [skupa podataka sa Twitch-a](https://clivecast.github.io/), što znači da jedan dokument predstavlja zapis o jednom prenosu u jednom trenutku posmatranja. Pored podataka direktno sadržanih u redovima iz skupa podataka dodat je podatak o vremenskom trenutku posmatranja (izvučen iz naziva datoteka skupa podataka), i dodatni podaci o video igri izvučeni iz kolekcije *games* (šablon proširene reference).

Primjer jednog dokumenta: <br> ![Dokument iz streams](./streams.PNG?raw=true "Dokument iz streams")
