# Sovelluksen käyttöönotto ja käyttö

Lataa uusin [julkaisu](https://github.com/SJET-Code/ot-harjoitustyo/releases) tietokoneellesi ja pura zip tiedosto sopivaan paikkaan.

## Tietokannan konfigurointi ja alustus

Jos haluat muuttaa tietokanta tiedoston nimeä (oletusnimi on database.db), voit muuttaa juurikansiosta löytyvää .env tiedostoa, josta löytyy rivi:
```DATABASE_FILENAME=database.db```, minkä voi muuttaa haluamaksesi tietokannan nimeksi. Jos haluat alustaa tietokannan (Ja menettää kaikki aikaisemmat highscoret),
voit suorittaa terminaalissa komennon ```poetry run invoke init-db```

## Pelin käynnistys

Kun olet juuri ladannut tiedoston, suorita terminaalissa ```poetry install```, kun olet pelin juurihakemistossa, riippuvuusten asentamiseksi.

Nyt voit tästä lähtien käynnistää pelin suorittamalla pelin juurihakemistossa terminaali komennon ```poetry run invoke start```

## Aloitusnäkymä

Peli lähtee käyntiin aloitusnäkymästä painamalla näppäimistön näppäintä 'N'.

![startscreen](https://user-images.githubusercontent.com/90755361/165077096-9966cc6c-79ed-406a-b32d-531af3412a24.png)

## Kierroksen alku

Kirroksen alussa pelaajan tulee valita panos (5 - pelaajan max crediitit) ja kuinka monta kättä haluaa pelata (1-3). Panos valitaa painamalla
nuolinäppäimiä ylös ja alas, ja panos kädelle vahvistetaan painamalla rivinvaihto näppäintä. Kierros alkaa kun pelaaja on asettanut ainakin yhdelle kädelle panoksen, ja painaa 'S' näppäintä, tai asettamalla kolmelle kädelle panokset ja painamalla rivinvaihto näppäintä.

![placingbetsstart](https://user-images.githubusercontent.com/90755361/166491256-ae23e7d3-5751-4336-aad6-e889b18c2207.png)

![placingbetsend](https://user-images.githubusercontent.com/90755361/166491423-10439d00-690c-422f-b3d2-0a184ebe55ef.png)

## Pelinäkymä

Pelinäkymällä pelaajan tulee valita kahdesta viiteen eri vaihtoehdosta joka käden kohdalla. Painamalla väli näppäintä pelaaja saa uuden kortin käteensä, kasvattaen käden yhteisarvoa, jos käden yhteisarvo ylittää arvon 21, pelaaja häviää tämän käden suoraan. Painamalla 'S' näppäintä pelaaja jää nykyisiin kortteihinsa ja pelivuoro siirtyy seuraavalle kädelle tai jakajalle. Jos pelaaja ei ole vielä nostanut muita kortteja käteensä kuin 2 alussa jaettua, hän voi painaa 'R' näppäintä antautuakseen käden, saaden näin puolet käden panoksesta takaisin. Näin ikään, jos pelaajan kädessä on vain 2 alussa saatua korttia, ja hänellä on tarpeeksi crediittejä, voi pelaaja tuplata kätensä panoksen painamalla 'D' näppäintä. Tuplauksen tehdessään pelaaja voi nostaa tähän käteen vain yhden kortin lisää, minkä jälkeen pelivuoro siirtyy. Jos 2 ensimmäistä korttia ovat saman arvoisia, ja pelaajalla on tarpeeksi crediittejä, hän voi jakaa tämän käden kahdeksi erilliseksi kädeksi painamalla rivinvaihto näppäintä. Tässä tilanteessa nämä kädet pelataan loppuun yksitellen, omilla panoksillaan. Punainen tausta osoittaa minkä käden pelivuoro on.

![gameoptions](https://user-images.githubusercontent.com/90755361/166493103-f02de046-2663-48f9-8280-88c89f705ca0.png)

![gamesplit](https://user-images.githubusercontent.com/90755361/166493375-3535e5b8-b234-49f1-8bde-32211faf4cdf.png)

Kun pelaajan kaikkien käsien pelivuorot on käsitelty, siirty pelivuoro jakajalle. Jakaja kääntää jakajankortin, ja jatkaa korttien nostamista, kunnes jakajan korttien yhteisarvo on 17 tai suurempi. Kun jakajan vuoro on käsitelty, tulee pelaajan käsien päälle ilmoitus lopputuloksesta, mahdollinen voitto tai häviö summa.

![roundresult](https://user-images.githubusercontent.com/90755361/166494106-33fd33be-544d-4aff-9710-de6ffdc3dd7a.png)

Nyt pelaaja voi valita uuden kierroksen ja pelipöydästä voittajana lähtemisen väliltä, jos pelaaja päättää lähteä vielä voiton puolella painamalla 'R' näppäintä, hänen crediittinsä kuvastavat hänen pisteitään tulostaulukossa.

![highscores](https://user-images.githubusercontent.com/90755361/166494983-ad88e976-25dc-44d0-87dd-88deebc4b3d0.png)

Jos pelaaja haluaa aloittaa uuden kierroksen, hän voi painaa väli näppäintä. Jos pelaajalla on vähemmän kuin 5 crediittiä kierroksen lopussa, hän häviää pelin, ja voi aloittaa uuden pelin painamalla 'N' näppäintä.

![newgame](https://user-images.githubusercontent.com/90755361/166495860-be0e4923-b99b-4c75-8a12-c02b22ce045d.png)

Pelistä poistutaan sulkemalla peli-ikkuna.
