#!/usr/bin/env python3

# file for the playing card object of 31 card game player

class Card:

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def getValue(self):
        if self.value > 10:
            return 10
        elif self.value == 1:
            return 11
        else:
            return self.value

    def printCard(self):
        if self.value == 1:
            print("Ace of " + self.suit)
        elif self.value == 11:
            print("Jack of " + self.suit)
        elif self.value == 12:
            print("Queen of " + self.suit)
        elif self.value == 13:
            print("King of " + self.suit)
        else:
            print(str(self.value) + " of " + self.suit)