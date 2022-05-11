# Testausdokumentti

Ohjelman toimivuutta testataan ohjelman oikeaa toimintaa simuloivilla yksikkötesteillä (unit testing), sekä manuaalisilla käyttöönotto ja toimintatesteillä.

## Yksikkötestit

Pelilogiikkaa testataan jokaisen pelilogiikka luokan omilla testi luokilla, eli ```Player```-luokkaa testataan ```TestPlayer```-luokalla jne.
Luokat ```Round```, ```Hand``` ja ```Deck``` testaavat myös monien luokkien yhdistelmiä, sillä näiden luokkien yhteistyö on pelilogiikan ytimessä.

Tietokannasta vastaavalle koodille ja ```ScoreRepository```-luokalle on myös testiluokka ```TestScoreRepository```.

### Testauskattavuus

Yksikkötestauksen haaraumajakauma on 94%, kun käyttöliittymän koodi on jätetty sen ulkopuolelle. En testannut käyttöliittymän luokkia, sillä ne eivät sovellu yksikkötestattavaksi, sillä haluttu toiminto on asettaa sprite olioita oikealle paikalle, ja piirtää niitä ruudulle, mitä ei yksikkötestuksessa saa mielekkäästi tarkastettua.

![Coverage report](https://user-images.githubusercontent.com/90755361/167908912-53fbf55c-8ba6-43a5-852d-5bb86c0835fb.png)

## Käyttöönotto

Ohjelman käyttöönotto ja knofigurointi onnistui käyttöohjetta seuraamalla, ohjelma on testattu MacOS Monterey Version 12.3.1 ja Linux Cubbli ympäristöissä.
Peliä pelatessa ei esiinny virheitä tai bugeja, eli peli toimii suunnitellusti ja määrittelydokumentin mukaisesti.