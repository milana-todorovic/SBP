# Uputstvo za upotrebu skripte za popunjavanje prve verzije baze

#### Pokretranje: <code>python fill_db.py</code>

#### Potrebni paketi

- [PyMongo](https://pymongo.readthedocs.io/en/stable/) <br> *Instalacija:* <code>pip install pymongo</code>   
- [dateutil](https://dateutil.readthedocs.io/en/stable/index.html) <br> *Instalacija:* <code>pip install python-dateutil</code>   

#### Očekivani parametri

Navedene parametre je moguće izmjeniti ispravkom datoteke *fill_db.py*. U slučaju izmjene parametara nije potrebno mijenjati *games.py* i *streams.py*.
- **Struktura direktorijuma:** Skripta očekuje da se datoteke iz [skupa podataka sa Twitch-a](https://clivecast.github.io/) nalaze u direktorijumu sa nazivom *twitch*, i da se datoteka *steam.csv* iz [skupa podataka sa Steam-a](https://www.kaggle.com/nikdavis/steam-store-games) nalazi u direktorijumu sa nazivom *steam games*. Očekivana struktura direktorijuma je prikazana na slici ispod. <br>
![Struktura direktorijuma](./dir.PNG?raw=true "Struktura direktorijuma")
- **Baza podataka:** Skripta očekuje da je MongoDB pokrenut na *localhost:27017*. Kreirana baza imaće naziv *sbp-v1*.
