import random

class Player:
    def __init__(self):
        self._credits = 100

    def bet(self,bet:int):
        if self._credits-bet>=0:
            self._credits-=bet
            return True
        else:
            return False
    
    def payout(self,payout:int):
        self._credits+=payout
    
    def credits(self):
        return self._credits
    
    def reset(self):
        self._credits = 100

class PlayingCard:
    def __init__(self,value:int,crest:str):
        self._value=value
        self._crest=crest #'S'=spades, 'C'=clubs, 'D'=diamonds, 'H'=hearts + number or type of facecard, 'A'=ace, 'J'=jack, 'Q'=queen, 'K'=king

    def value(self):
        return self._value

    def crest(self):
        return self._crest
    
    def ace_change(self):
        if self._value==11:
            self._value=1


crests=['S','C','D','H']
deck=[]
for crest in crests:
    for i in range(2,15):
        if i==11:
            deck.append(PlayingCard(10,crest+'J'))
        elif i==12:
            deck.append(PlayingCard(10,crest+'Q'))
        elif i==13:
            deck.append(PlayingCard(10,crest+'K'))
        elif i==14:
            deck.append(PlayingCard(11,crest+'A'))
        else:
            deck.append(PlayingCard(i,crest+str(i)))

random.shuffle(deck)

class Deck:
    def __init__(self):
        self._deck=deck.copy()
        self._size=len(self._deck)

    def shuffle(self):
        self._deck=deck.copy()
        random.shuffle(self._deck)
        self._size=len(self._deck)

    def get_card(self):
        card=self._deck.pop()
        self._size=len(self._deck)
        if self._size<13:
            self.shuffle()
        return card

class Round:
    def __init__(self, player:Player, deck:Deck):
        self._player=player
        self._deck=deck
        self._dealer_hand=[]
        self._player_hand=[]
        self._dealer_hand_value=0
        self._player_hand_value=0
        self._bet=5
    
    def new_round(self,bet:int):
        self.reset()
        player_bet=self._player.bet(bet)
        if player_bet:
            self._bet=bet
            card=self._deck.get_card()
            self._dealer_hand.append(card)
            self._dealer_hand_value+=card.value()
            self._dealer_card=self._deck.get_card()
            card=self._deck.get_card()
            self._player_hand.append(card)
            self._player_hand_value+=card.value()
        else:
            return False

    def hit(self):
        card=self._deck.get_card()
        self._player_hand_value+=card.value()
        self._player_hand.append(card)
        if self._player_hand_value>21:
            for c in self._player_hand:
                if c.value()==11:
                    c.ace_change()
                    self._player_hand_value-=10
                    break
            
    def stay(self):
        self._dealer_hand_value+=self._dealer_card.value()
        self._dealer_hand.append(self._dealer_card)

    def dealer_deal(self):
        if self._dealer_hand_value<17:
            card=self._deck.get_card()
            self._dealer_hand_value+=card.value()
            self._dealer_hand.append(card)
            if 17<=self._dealer_hand_value<=21:
                return self.check_winner()
            elif self._dealer_hand_value>21:
                for c in self._dealer_hand:
                    if c.value()==11:
                        c.ace_change()
                        self._dealer_hand_value-=10
                        break
                if 17<=self._dealer_hand_value<=21:
                    return self.check_winner()
        else:
            return self.check_winner()


    def end_round(self,win:bool):
        if win:
            if self._player_hand_value==21 and len(self._player_hand)==2 and self._dealer_hand_value!=21:
                payout=int(self._bet+self._bet*3/2)
                self._player.payout(payout)
            elif self._player_hand_value==21 and len(self._player_hand)==2 and self._dealer_hand_value==21 and len(self._dealer_hand)==2:
                self._player.payout(self._bet)
            else:
                payout=self._bet*2
                self._player.payout(payout)
        
    def reset(self):
        self._dealer_hand=[]
        self._player_hand=[]
        self._dealer_hand_value=0
        self._player_hand_value=0

    def check_winner(self):
        if self._dealer_hand_value>21:
            self.end_round(True)
            return True
        if self._dealer_hand_value==21==self._player_hand_value:
            self.end_round(True)
            return True
        elif self._dealer_hand_value>=self._player_hand_value:
            self.end_round(False)
            return False
        else:
            self.end_round(True)
            return True

    def player_hand(self):
        return self._player_hand, self._player_hand_value

    def dealer_hand(self):
        return self._dealer_hand, self._dealer_hand_value