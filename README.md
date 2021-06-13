# Projekat iz predmeta SBP

***Tema:***  Analiza popularnosti video igara pomoću podataka o prenosima sa Twitch-a</td>

***Autori:***  Ana Perišić RA1/2017, Milana Todorović RA3/2017


#### Opis skupa podataka

Za potrebe projekta korištena su dva skupa podataka:
- [Skup podataka o video igrama](https://www.kaggle.com/nikdavis/steam-store-games) <br> Skup sadrži podatke o 27000 video igara prikupljene sa Steam-a. Korištena je datoteka iz skupa sa osnovnim informacijama o video igrama (*steam.csv*). Detaljniji opis podataka sadržanih u skupu može se pronaći u [prijedlogu projekta](https://github.com/milana-todorovic/SBP/blob/main/predlog%20projekta.pptx).
- [Skup podataka o prenosima sa Twitch-a](https://clivecast.github.io/) <br> Skup podataka je sastavljen tako što su 2015. godine u periodu od 1.2. do 3.7. svakih 5 minuta prikupljani podaci o svim aktivnim prenosima na Twitch-u. Prikupljeni podaci uključuju detalje o autoru prenosa, video igru igranu u prenosu u posmatranom trenutku, i podatke o gledanosti u posmatranom trenutku (detaljniji opis strukture skupa podataka dostupan je u [prijedlogu projekta](https://github.com/milana-todorovic/SBP/blob/main/predlog%20projekta.pptx)). Veličina inicijalnog skupa podataka je oko 17gb. Za potrebe projekta korišten je manji podskup skupa (podaci prikupljeni od 1.2. do 20.2.). Takođe su iz skupa podataka izbačeni svi podaci koje nije bilo moguće povezati sa skupom podataka o video igrama.

## Rezultati 

#### Šeme baze podataka

Za potrebe projekta kreirane su dvije šeme baze podataka, pri čemu je glavni cilj pri kreiranju druge šeme bio poboljšanje performansi upita.

Inicijalna šema baze podataka prati strukturu skupa podataka. Detaljan opis inicijalne šeme dostupan je u [v1/schema](./v1/schema). Za upis podataka iz skupa podataka u bazu korištena je Python skripta, koja se zajedno sa uputstvom za pokretanje nalazi u [v1/scripts](./v1/scripts).

Druga šema baze podataka kreirana je transformacijom prve šeme, uz upotrebu šablona baketiranja i proračunavanja. U drugoj šemi su takođe podignuti indeksi nad pojedinim poljima. Detaljan opis druge šeme dostupan je u [v2/schema](./v2/schema), a skripta za kreiranje šeme sa uputstvom za pokretanje u [v2/scripts](./v2/scripts).

#### Upiti

1. Pronaći 10 igrica koje su imale najviše gledalaca u jednom trenutku (u okviru svih prenosa koji su u tom trenutku bili aktivni).
2. Za svakog autora odrediti koju je igru igrao najveći broj minuta.
3. Za svaki sat u danu pronaći koja je igra imala u prosjeku najviše prenosa.
4. Koje igre je prenosio autor koji je ostvario najveći rast broja pratilaca u posmatranom vremenskom periodu?
5. Koje žanrove je prenosio najveći broj autora?
6. Za svaku igru odrediti koliko različitih autora je igralo u bar jednom prenosu, i pronaći 3 autora koja su je igrala u najviše prenosa.
7. Pronaći 5 igara koje su prenošene najveći broj minuta.
8. Koliki je broj prenosa, i prosjek, minimum, i maksimum prosječnog broja gledalaca po prenosu za svaku igru?
9. Za svaki žanr odrediti prosječno i maksimalno trajanje prenosa, i prosječni broj gledalaca po prenosu.
10. Za sve autore koji su najveći broj minuta igrali igru The Evil Within, a pored toga su igrali bar još jednu igru, pronaći koje su još igre igrali, u koliko prenosa, koliko ukupno minuta, i koliko minuta u prosjeku po prenosu.

Detalji imlementacije upita nad prvom šemom dostupni su u [v1/queries](./v1/queries), a detalji implementacije nad drugom šemom u [v2/queries](./v2/queries).

#### Performanse
