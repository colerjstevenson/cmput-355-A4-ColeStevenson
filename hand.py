#!/usr/bin/env python3
# file for deck object for 31 card game player

import card

class Hand:

    def __init__(self):
        self.cards = []

    # adds card c to hand
    def addCard(self, c):
        self.cards.append(c)

    # removes card at position p from hand and returns it
    def takeCard(self, p):
        return self.cards.pop(p)

    def printHand(self, turn):
        if turn == 'player':
            print("The cards in your hand are:")
        else:
            print("The card in the computers hand are:")
        
        for i in range(len(self.cards)):
            print("   " + str(i+1) + ". ", end = '')
            self.cards[i].printCard()

    # returns the score of the hand
    def getScore(self) -> int:
        if self.cards[0].suit == self.cards[1].suit and self.cards[1].suit == self.cards[2].suit:
            return self.cards[0].getValue() + self.cards[1].getValue() + self.cards[2].getValue()
        else:
            scores = []
            scores.append(self.cards[0].getValue())
            scores.append(self.cards[1].getValue())
            scores.append(self.cards[2].getValue())
            if self.cards[0].suit == self.cards[1].suit:
                scores.append(self.cards[0].getValue() + self.cards[1].getValue())
            if self.cards[1].suit == self.cards[2].suit:
                scores.append(self.cards[1].getValue() + self.cards[2].getValue())
            if self.cards[0].suit == self.cards[2].suit:
                scores.append(self.cards[0].getValue() + self.cards[2].getValue())

            return max(scores)
    
    # if c is in the hand it is removed
    def ifInHandRemove(self, c):
        for card in self.cards:
            if c.value == card.value and c.suit == card.suit:
                self.cards.remove(card)