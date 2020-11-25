#!/usr/bin/env python3

# file for the computer opponent object of 31 card game player

from scipy.stats import hypergeom
import deck, hand, card 

class Computer:

    def __init__(self):
        self.possible_deck = deck.Deck()
        self.possible_deck.fillDeck()
        self.known_player_hand = hand.Hand()
        self.draws = 3

    
    # if c hasnt been seen yet we remove it from possible deck
    def seenCard(self, c):
        for i in range(len(self.possible_deck.cards)):
            if c.value == self.possible_deck.cards[i].value and c.suit == self.possible_deck.cards[i].suit:
                self.possible_deck.getCard(i)
                return 1
        return 0

    # add card to known hand
    def addKnown(self, c):
        self.known_player_hand.addCard(c)

    # if c is in known hand we remove it
    def checkKnown(self, c):
        for i in range(len(self.known_player_hand.cards)):

            if c.value == self.known_player_hand.cards[i].value and c.suit == self.known_player_hand.cards[i].suit:
                self.known_player_hand.takeCard(i)
                return 1
        return 0

    # adds 1 to the number of draws
    def addTurn(self):
        self.draws += 1

    # reset seen cards when deck reshuffle
    def reset(self, hand, top):
        self.draws = 6
        self.possible_deck = deck.Deck()
        self.possible_deck.fillDeck()
        for c in hand.cards:
            self.seenCard(c)

        for c in self.known_player_hand.cards:
            self.seenCard(c)

        self.seenCard(top)

    


    # returns the probability of the players hand being higher than score
    def prob(self, score):
        
        prob = 0.0

        if len(self.known_player_hand.cards) == 0:
            for i in range(len(self.possible_deck.cards)):
                for j in range(i, len(self.possible_deck.cards)):
                    for k in range(j, len(self.possible_deck.cards)):
                        test = hand.Hand()
                        test.addCard(self.possible_deck.cards[i])
                        test.addCard(self.possible_deck.cards[j])
                        test.addCard(self.possible_deck.cards[k])
                        
                        if test.getScore() >= score:
                            prob += hypergeom.pmf(3, 52, 3, self.draws)
        
        elif len(self.known_player_hand.cards) == 1:
            for i in range(len(self.possible_deck.cards)):
                for j in range(i, len(self.possible_deck.cards)):
                    test = hand.Hand()
                    test.addCard(self.possible_deck.cards[i])
                    test.addCard(self.possible_deck.cards[j])
                    test.addCard(self.known_player_hand.cards[0])

                    if test.getScore() >= score:
                            prob += hypergeom.pmf(2, 52, 2, self.draws)

        elif len(self.known_player_hand.cards) == 2:
            for i in range(len(self.possible_deck.cards)):
               
                test = hand.Hand()
                test.addCard(self.possible_deck.cards[i])
                test.addCard(self.known_player_hand.cards[0])
                test.addCard(self.known_player_hand.cards[1])

                if test.getScore() >= score:
                        prob += hypergeom.pmf(1, 52, 1, self.draws)

        else:
            if self.known_player_hand.getScore() >= score:
                prob = 1000.0
            else:
                prob = 0.0

        return prob

    def numberOfHigh(suit):
        count = 0
        for card in possible_deck.cards:
            if card.getValue >= 8 and card.suit == suit:
                count += 1
            
        return count
    


    # records data about the play state in a data.txt
    def record(self, playerHand, compHand):
        f = open("data.txt", 'a')
        score = compHand.getScore()
        if score > playerHand.getScore():
            f.write(str(self.prob(score)) + ", " + str(compHand.getScore()) + ", "+ str(playerHand.getScore()) + ", " + str(self.draws) + ", 1, "+ str(len(self.known_player_hand.cards)) + "\n" )
        else:
            f.write(str(self.prob(score)) + ", " + str(compHand.getScore()) + ", "+ str(playerHand.getScore()) + ", " + str(self.draws) + ", 0, "+ str(len(self.known_player_hand.cards)) + "\n" )

        f.close()


    # return the position of the card the should be discarded to give the best hand
    def bestDiscard(self, h, type, score):
        bestPos = 3
        bestValue = 9999
        bestScore = score
        
        if type == "deck":
            for i in range(4): 
                temp = h.cards[i]
                check = hand.Hand()
                for j in range(4):
                    if j != i:
                        check.addCard(h.cards[j])
   
                if check.getScore() > bestScore:
                   
                    bestScore = check.getScore()
                    bestPos = i
                    bestValue = temp.getValue()
                    bestSuit = temp.suit
                elif check.getScore() == bestScore:
                    if temp.getValue() < bestValue:
                        bestScore = check.getScore()
                        bestPos = i
                        bestValue = temp.getValue()
                        bestSuit = temp.suit

                
        else:
            for i in range(4): 
                temp = h.cards[i]
                check = hand.Hand()
                for j in range(4):
                    if j != i:
                        check.addCard(h.cards[j])
         
                if check.getScore() > bestScore:
                    bestScore = check.getScore()
                    bestPos = i
                    bestValue = temp.getValue()
                    bestSuit = temp.suit
                elif temp.getValue() < 6 and check.getScore() == bestScore:
                        if temp.getValue() < bestValue and temp.getValue() <= 7:
                            bestScore = check.getScore()
                            bestPos = i
                            bestValue = temp.getValue()
                            bestSuit = temp.suit
                    
        return bestPos


    

             
