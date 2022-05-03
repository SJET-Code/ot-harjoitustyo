# Sovelluksen Arkkitehtuuri

## Luokkadiagrammi

![classdiagram](https://user-images.githubusercontent.com/90755361/166474607-5deae4c4-de6e-48eb-b87c-94d8be23fc19.png)

## Sovelluslogiikka

Pelin sovelluslogiikka on jaettu käyttöliittymän eli pelinäkymän muodostaviin kansion ui luokkiin, ja pelilogiikan luokista muodostuvaan kansioon blackjack.

### Pelilogiikka

Pelilogiikka perustuu luokan Round ympärille. Round luokka kuvastaa yhtä blackjack kierrosta, ja hyödyntää kaikkia muita pelilogiikan luokkia. Luokka Hand kuvastaa yhtä pelaajan pelaamaa kättä. Luokka Player huolehtii pelaajan crediiteistä, kun taas luokka Deck kuvastaa korttipakkaa, josta nostetaan PlayinCard luokan kuvastavia peli kortteja.

### Käyttöliittymälogiikka

Käyttöliittymä muodostuu luokan GameLoop ympärille. GameLoop hyödyntää luokkaa Board, mikä asettelee peli-elementit oikeille paikoille pelitilanteen perusteella.
Luokka EventQueue havaitsee pelaajan näppäimistön komennot, ja välittää ne GameLoopin funktioille. Luokka Renderer piirtää Sprite-oliot pelaajan näytölle luokan Clock määrittällä nopeudella.

## Pelin toiminnallisuus

### Uuden pelin aloitus

Käyttäjällä on seuraava näkymä aloitusruudussa, ja sekvenssi alkaa käyttäjän painamalla näppäin 'N'

![startscreen](https://user-images.githubusercontent.com/90755361/165077096-9966cc6c-79ed-406a-b32d-531af3412a24.png)

```mermaid
sequenceDiagram
  actor U as User
  participant GL as GameLoop
  participant B as Board
  participant Ren as Renderer
  participant P as Player
  participant E as EventQueue
  loop rendering start sprites
    Ren->>Ren: draw start sprites
  end
  Note right of Ren: Renderer gets information on what sprites<br/>to draw from the Board class dictionary "state"
  U->>E: Press "N"
  E->>GL: event.key == pygame.K_n
  GL->GL: n_button_actions()
  GL->>P: reset()
  P->P: credits = 100
  GL->>B: start_game()
  B->B: switch the state to "game" and add the deck sprite to game sprites
  loop rendering game sprites
    Ren->>Ren: draw game sprites
  end
```


