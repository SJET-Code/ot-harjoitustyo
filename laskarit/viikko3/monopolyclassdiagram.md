```mermaid
classDiagram
	class Monopoli{
	}
	class Noppa{
    	    +heitto() int
	}
	class PeliLauta{
	}
	class Pelaaja{
	}
	class PeliRuutu{
	}
	class PeliNappula{
	}
	Monopoli '1' --> '2' Noppa
	Monopoli '1' --> '2..8' Pelaaja
	Monopoli '1' --> '1' PeliLauta
	Pelaaja '1' --> '1' PeliNappula
	PeliLauta '1' --> '2..8' PeliNappula
	PeliLauta '1' --> '40' PeliRuutu
	PeliRuutu '1' --> '0..8' PeliNappula
	PeliRuutu '1' --> '1' PeliRuutu
	PeliNappula '1' --> '1' PeliRuutu
	
```
