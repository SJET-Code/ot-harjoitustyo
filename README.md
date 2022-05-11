# BlackJackApp

Sovellus simuloi tunnettua casino peliä [Blackjack](https://fi.wikipedia.org/wiki/Blackjack)!
Peli kulkee kierroksina, joiden alussa pelaaja asettaa haluamansa panoksen pelin sisäisiä crediittejä.
Tavoitteena on saada pelikorteista luku mahdollisimman lähelle arvoa 21, ylittämättä tätä arvoa.
Vastustajana toimii jakaja. Peli jatkuu niin pitkään kun crediittejä riittää, tai kunnes pelaaja päättää lopettaa.

## Dokumentaatio

- [Käyttöohje](./dokumentaatio/kayttoohje.md)

- [Vaativuusmäärittely](./dokumentaatio/vaatimusmaarittely.md)

- [Tuntikirjanpito](./dokumentaatio/tuntikirjanpito.md)

- [Credits](./dokumentaatio/credits.md)

- [Changelog](./dokumentaatio/changelog.md)

- [Arkkitehtuuri](./dokumentaatio/arkkitehtuuri.md)

- [Testausdokumentti](./dokumentaatio/testaus.md)

## Asennus

Voit testata sovellusta kloonaamalla tämän repon ja ajamalla komennot:
```
poetry install
poetry run invoke start
```

## Tietokannan alustus

Jos haluat tyhjentää tietokannan pisteistä, aja komento:
```
poetry run invoke init-db
```
## Testien suoritus
Voit suorittaa testit ja saada testikattavuus raportin komennoilla:
```
poetry run invoke test
poetry run invoke coverage-report
```
## Pylint tarkistus
Voit tarkistaa koodin tyylin pylintilla, ajamalla komennon
```
poetry run invoke lint
```
## Releases
- [viikko 5 release](https://github.com/SJET-Code/ot-harjoitustyo/releases/tag/viikko5)
- [viikko 6 release](https://github.com/SJET-Code/ot-harjoitustyo/releases/tag/viikko6)
