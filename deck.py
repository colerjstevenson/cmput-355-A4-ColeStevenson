#!/usr/bin/env python3
# file for deck object for 31 card game player

import card, random

class Deck:

    def __init__(self):
        self.cards = []

    
    # fills the deck with 52 new cards and shuffles them
    def fillDeck(self):
        for s in range(1,5):
            for v in range(1, 14):
                if s == 1:
                    self.cards.append(card.Card(v, "Hearts"))
                if s == 2:
                    self.cards.append(card.Card(v, "Diamonds"))
                if s == 3:
                    self.cards.append(card.Card(v, "Clubs"))
                if s == 4:
                    self.cards.append(card.Card(v, "Spades"))

        random.shuffle(self.cards)

    # take the top card from the deck
    def takeCard(self):
        return self.cards.pop(0)

    def getCard(self, p):
        return self.cards.pop(p)


    # tells you what the top card of the deck is
    def topCard(self):
        return self.cards[0]
    
    # puts card c on top of the deck
    def addCard(self, c):
        self.cards.insert(0, c)

    # returns the number of cards in the deck
    def cardsLeft(self):
        return len(self.cards)

    # if c is in the deck it is removed
    def ifInDeckRemove(self, c):
        for card in self.cards:
            if c.value == card.value and c.suit == card.suit:
                self.cards.remove(card)

    def get(self, i):
        return self.cards[i]
        