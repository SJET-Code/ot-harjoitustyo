# Vaativuusmäärittely

## Sovelluksen tarkoitus

Sovellus simuloi klassista blackjack korttipeliä, minkä tarkemmat säännöt voi lukea [täältä](https://fi.wikipedia.org/wiki/Blackjack).
Pelaaja pelaa siis jakajaa vastaan, ja asettaa joka kierros panoksen, ennen korttien jakoa. Peli jatkuu niin kauan kuin pelaajalla on crediittejä asettaa panokseksi,
tai kunnes pelaaja päättää lopettaa, milloin lopullinen rahamäärä kuvastaa hänen pisteitään.

## Käyttöliittymäluonnos

Sovelluksen käyttöliittymä koostuu alkunäytöstä, pelinäkymästä, ja lopetusnäkymästä.

- Alkunäytöllä voidaan aloittaa uusi peli.
- Pelinäkymässä valitaan kaikki blackjack kierrokseen kuuluvat valinnat:
  - Kuinka monta kättä pelaaja haluaa pelata kierroksella, ja millä panoksilla
  - Nähdään jaetut kortit, ja valitaan pelin kulkuun liittyviä valintoja (tuplaus, uuden kortin nosto, jne.)
  - Valitaan kierroksen lopussa halutaanko pelata uusi kierros, aloittaa uusi peli, vai lopettaa peli ja tallentaa tulos (retire)
- Loppunäkymässä nähdään korkeimmat pisteet, voidaan tallentaa tulos nimimerkillä varustettuna tähän listaan, sekä voidaan aloittaa uusi peli.

## Pelin toiminnallisuudet

- [x] Pelaaja voi aloittaa uuden blackjack pelin 
  - uuden pelin alussa pelaaja saa 100 crediittiä

- [x] Pelaaja voi asettaa panoksen uuden kierroksen alkaessa
  - minimipanos on 5 crediittiä, maksimipanos on pelaajan crediittien määrä
  
- [x] Pelaajalle jaetaan kaksi korttia, jonka jälkeen pelaaja voi valita haluaako hän nostaa uuden kortin, vai jäädä nykyisiin kortteihin.
  - mikäli pelaaja nostaa uuden kortin ja pelaajan korttien yhteisarvo on > 21, pelaaja häviää kierroksen ja menettää panoksensa
  - mikäli pelaaja tai jakaja nostaa ässän, on ässän arvo aina 11, kunnes pelaajan käden yhteisarvo on > 21, milloin ässän arvoksi tulee 1

- [x] Kierroksen loputtua pelaaja häviää pelin, jos hänellä on < 5 crediittiä
  - pelaaja voi myös lopettaa pelin halutessaan, tai pelata uuden kierroksen, jos hänellä on >= 5 crediittiä

- [x] Pelin lopetettuaan, pelaaja saa näkymän korkeimmista pisteistä, ja voi tallentaa oman tuloksensa nimimerkillä (3 kirjainta)
  - pelaajan crediitit kuvastavat hänen pisteitään

- [x] Pelaajalla on mahdollisuus tuplata, jakaa ja antautua käsi tiettyjen [ehtojen](https://fi.wikipedia.org/wiki/Blackjack#Tuplaus_(Double)) täytyttyä

- [x] Pelaajalla on mahdollisuus pelata useita käsiä samaan aikaan eri panoksilla
  - Kierroksen alussa on mahdollista asettaa panos korkeintaan kolmelle eri kädelle, ja niistä käsistä voi jakaa korkeintaan kaksi kättä, pelatakseen siis enintään viisi kättä kerrallaan
