# Uputstvo za upotrebu skripte za popunjavanje druge verzije baze

Druga verzija baze dobijena je transformacijom prve verzije pomoću Mongo upita. Nova baza kreirana na ovaj način imaće naziv *sbp-v2*. 

#### Redosled izvršavanja upita:

1. *transform-database-1.js* <br> Upite iz ove skripte potrebno je izvršiti nad prvom verzijom baze. Kreiraće se kolekcije *games*, *streams*, *broadcasters*, i *games-per-time*.
2. *transform-database-2.js* <br> Upit iz ove skripte se izvršava nad novokreiranom bazom (*sbp-v2*). Kreiraće se kolekcija *games-broadcasters"*. 
3. *indexes.js* <br> Upiti se izvršavaju nad novokreiranom bazom, i dodaju indekse za kolekciju *games-broadcasters"*. 
