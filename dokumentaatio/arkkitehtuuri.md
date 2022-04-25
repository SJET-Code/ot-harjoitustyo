# Sovelluksen Arkkitehtuuri

## Luokkadiagrammi

![classdiagram](https://user-images.githubusercontent.com/90755361/162941854-de2bd216-9e61-487c-aecc-51c1d12b70d9.png)

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
  participant R as Round
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


