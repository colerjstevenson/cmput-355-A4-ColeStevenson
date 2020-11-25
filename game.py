#!/usr/bin/env python3

# This main file for the 31 card game player created by Cole Stevenson
# for assignment 4 of cmput 355 for the fall semester

import deck, hand, card, computer, random


# plays game, returns 1 if human wins, returns 0 if computer wins
def play():
    knock = 0

    #create computer player
    comp = computer.Computer()

    # create new deck
    drawDeck = deck.Deck()
    drawDeck.fillDeck()

    # deal 3 cards to each player
    playerHand = hand.Hand()
    compHand = hand.Hand()
    for i in range(3):
        playerHand.addCard(drawDeck.takeCard())
        temp = drawDeck.takeCard()
        compHand.addCard(temp)
        comp.seenCard(temp)

    # create discard pile and puts top card from deck in it
    discardPile = deck.Deck()
    temp = drawDeck.takeCard()
    discardPile.addCard(temp)
    comp.seenCard(temp)

    #alternate turns
    while knock == 0:
        
        # PLAYER 1 TURN
        print("\nIT IS YOUR TURN\n")
        
        playerHand.printHand('player')

        
        print("\nThe top card of the discard pile is the:")
        discardPile.topCard().printCard()
        
        print('\nWhat would you like to do?')
        print('   1. Take card from Discard Pile')
        print('   2. Draw card from Deck')
        print('   3. Knock (End Round)')
        move = input("(1, 2, or 3?)")
        while(move != '1' and move != '2' and move != '3'):
            print("INVALID RESPONSE")
            move = input("\n(1, 2, or 3?)")

            
        if move == '1': # take from discard
            temp = discardPile.takeCard()
            playerHand.addCard(temp)
            comp.addKnown(temp)

            print(' ')
            playerHand.printHand('player')

            print("\nWhich card would you like to discard?")
            dis = input("(1, 2, 3, or 4?)")
            while(dis != '1' and dis != '2' and dis != '3' and dis != '4'):
                print("INVALID RESPONSE")
                dis = input("\n(1, 2, 3, or 4?)")
                
            
            temp = playerHand.takeCard(int(dis)-1)
            discardPile.addCard(temp)
            comp.checkKnown(temp)
            comp.seenCard(temp)
            
        
        elif move == '2': # take from deck
            comp.addTurn()

            temp = drawDeck.takeCard()
            playerHand.addCard(temp)
            comp.seenCard(temp)

            print(' ')
            playerHand.printHand('player')

            print("\nWhich card would you like to discard?")
            dis = input("(1, 2, 3, or 4?)")
            while(dis != '1' and dis != '2' and dis != '3' and dis != '4'):
                print("INVALID RESPONSE")
                dis = input("\n(1, 2, 3, or 4?)")
            
            temp = playerHand.takeCard(int(dis)-1)
            discardPile.addCard(temp)
            comp.checkKnown(temp)
            comp.seenCard(temp)

           
                
        
        else:  # knock
            knock = 1
            continue

        if drawDeck.cardsLeft() == 0:
            print("OUT OF CARDS! RESHUFFLING DISCARDS PILE")
            while discardPile.cardsLeft() != 0:
                drawDeck.addcard(discardpile.takeCard())
            random.shuffle(drawDeck.cards)
            discardPile.addCard(drawDeck.takeCard())
            comp.reset(compHand, discardPile.topCard())


        if knock != 0 or playerHand.getScore() == 31:
            knock = 1
            continue
        
        
        # COMPUTER TURN
        print("\nIT IS THE COMPUTER`S TURN")

        if float(compHand.getScore())/float(comp.draws) > 12.0/(comp.draws**0.6) or comp.prob(compHand.getScore()) < 0.35 or compHand.getScore() >= 27.0:
            print("\nCOMPUTER KNOCKED\n")   # check if we should knock
            knock = 2
            continue
        
        temp = compHand.getScore()
        compHand.addCard(discardPile.takeCard())
        check = comp.bestDiscard(compHand, "pile", temp)                  #check if flipped card helps hand
        discardPile.addCard(compHand.takeCard(check))
        if check != 3:
            print("\nCOMPUTER TOOK FROM DISCARD PILE\n")
        else:
            print("\nCOMPUTER TOOK FROM DREW A CARD FROM THE DECK\n")
            compHand.addCard(drawDeck.takeCard())
            check = comp.bestDiscard(compHand, "deck", temp)                      # draw from deck
            comp.seenCard(compHand.cards[check])
            discardPile.addCard(compHand.takeCard(check))

        if drawDeck.cardsLeft() == 0:
            print("\nOUT OF CARDS! RESHUFFLING DISCARDS PILE\n")
            while discardPile.cardsLeft() != 0:
                drawDeck.addCard(discardPile.takeCard())
            random.shuffle(drawDeck.cards)
            discardPile.addCard(drawDeck.takeCard())
            comp.reset(compHand, discardPile.topCard())

        if knock != 0 or playerHand.getScore() == 31:
            knock = 2
            continue
       


        




    
    # print results
    print('\nEND OF GAME')
    playerHand.printHand('player')
    print('Score: ' + str(playerHand.getScore()) + '\n')
    compHand.printHand('computer')
    print('Score: ' + str(compHand.getScore()) + '\n')


    f = open("winHumanData.txt", "a")
    # check hands
    if compHand.getScore() > playerHand.getScore():
        print('THE COMPUTER WINS!')
        f.write(str(compHand.getScore()) + ", " + str(playerHand.getScore()) + ", 1, " + str(knock) + ', ' + str(float(compHand.getScore())/float(comp.draws)) + ", " + str(comp.prob(compHand.getScore())) + "\n")
        f.close()
        return 0
    elif compHand.getScore() == playerHand.getScore():
        if knock == 1:
            print('THE COMPUTER WINS!')
            f.write(str(compHand.getScore()) + ", " + str(playerHand.getScore()) + ", 1, " + str(knock) + ', ' + str(float(compHand.getScore())/float(comp.draws)) + ", " + str(comp.prob(compHand.getScore())) + "\n")
            f.close()
            return 0

    print('YOU WIN!')
    f.write(str(compHand.getScore()) + ", " + str(playerHand.getScore()) + ", 0, " + str(knock) + ', ' + str(float(compHand.getScore())/float(comp.draws)) + ", " + str(comp.prob(compHand.getScore())) + "\n")
    f.close()
    return 1


# play game with two random players n times to collect data
def randomPlay(n):
    knock = 0
    count = 0

    #create computer player
    comp1 = computer.Computer()
    comp2 = computer.Computer()

    # create new deck
    drawDeck = deck.Deck()
    drawDeck.fillDeck()

    # deal 3 cards to each player
    playerHand = hand.Hand()
    compHand = hand.Hand()
    for i in range(3):
        temp = drawDeck.takeCard()
        playerHand.addCard(temp)
        comp1.seenCard(temp)

        temp = drawDeck.takeCard()
        compHand.addCard(temp)
        comp1.seenCard(temp)

    # create discard pile and puts top card from deck in it
    discardPile = deck.Deck()
    temp = drawDeck.takeCard()
    discardPile.addCard(temp)
    comp1.seenCard(temp)
    comp2.seenCard(temp)

    #alternate turns
    while knock == 0 and count < n:
        count += 1
        # PLAYER 1 TURN
        comp2.checkKnown(discardPile.topCard())
        comp2.seenCard(discardPile.topCard())
        print("IT IS P1 TURN\n")
        
        playerHand.printHand('player')
        
        print("\nThe top card of the discard pile is the:")
        discardPile.topCard().printCard()
        
        print('\nWhat would you like to do?')
        print('   1. take card from discard pile')
        print('   2. draw card from deck')
        print('   3. knock')
        move = str(random.randint(1,2))
        
            
        if move == '1': # take from discard
            temp = discardPile.takeCard()
            playerHand.addCard(temp)
            comp1.addKnown(temp)

            print(' ')
            playerHand.printHand('player')

            print("\nWhich card would you like to discard?")
            dis = str(random.randint(1,3))
                
            
            temp = playerHand.takeCard(int(dis)-1)
            discardPile.addCard(temp)
            comp1.checkKnown(temp)
            comp1.seenCard(temp)
            
        
        elif move == '2': # take from deck
            comp1.addTurn()

            temp = drawDeck.takeCard()
            playerHand.addCard(temp)
            comp1.seenCard(temp)

            print(' ')
            playerHand.printHand('player')

            print("\nWhich card would you like to discard?")
            dis = str(random.randint(1,3))
            
            temp = playerHand.takeCard(int(dis)-1)
            discardPile.addCard(temp)
            comp1.checkKnown(temp)
            comp1.seenCard(temp)

            if drawDeck.cardsLeft() == 0:
                print("OUT OF CARDS! RESHUFFLING DISCARDS PILE")
                while discardPile.cardsLeft() != 0:
                    drawDeck.addCard(discardpile.takeCard())
                random.shuffle(drawDeck.cards)
                discardPile.addCard(drawDeck.takeCard())
                comp1.reset(compHand, discardPile.topCard())
                comp2.reset(playerHand, discardPile.topCard())
        
        else:  # knock
            knock = 1
            continue
        
        
        # PLAYER 2 TURN
        print("IT IS P1 TURN\n")
        
        compHand.printHand('player')
        
        print("\nThe top card of the discard pile is the:")
        discardPile.topCard().printCard()
        
        print('\nWhat would you like to do?')
        print('   1. take card from discard pile')
        print('   2. draw card from deck')
        print('   3. knock')
        move = str(random.randint(1,2))
        
        
        
            
        if move == '1': # take from discard
            temp = discardPile.takeCard()
            compHand.addCard(temp)
            comp2.addKnown(temp)

            print(' ')
            compHand.printHand('player')

            print("\nWhich card would you like to discard?")
            dis = str(random.randint(1,3))
            
            temp = compHand.takeCard(int(dis)-1)
            discardPile.addCard(temp)
            comp2.checkKnown(temp)
            comp2.seenCard(temp)
        
        elif move == '2': # take from deck
            comp2.addTurn()

            temp = drawDeck.takeCard()
            compHand.addCard(temp)
            comp2.seenCard(temp)

            print(' ')
            compHand.printHand('player')

            print("\nWhich card would you like to discard?")
            dis = str(random.randint(1,3))
            
            
            temp = compHand.takeCard(int(dis)-1)
            discardPile.addCard(temp)
            comp2.checkKnown(temp)
            comp2.seenCard(temp)

            if drawDeck.cardsLeft() == 0:
                print("OUT OF CARDS! RESHUFFLING DISCARDS PILE")
                while discardPile.cardsLeft() != 0:
                    drawDeck.addCard(discardpile.takeCard())
                random.shuffle(drawDeck.cards)
                discardPile.addCard(drawDeck.takeCard())
                comp1.reset(compHand, discardPile.topCard())
                comp2.reset(playerHand, discardPile.topCard())
        
        else:  # knock
            knock = 2
            continue

        comp1.record(playerHand, compHand)
        #comp2.record(compHand, playerHand)
        
        
        
    print("done")


# play game with two human player to test mechanics
def testPlay():
    knock = 0

    #create computer player
    comp = computer.Computer()

    # create new deck
    drawDeck = deck.Deck()
    drawDeck.fillDeck()

    # deal 3 cards to each player
    playerHand = hand.Hand()
    compHand = hand.Hand()
    for i in range(3):
        playerHand.addCard(drawDeck.takeCard())
        temp = drawDeck.takeCard()
        compHand.addCard(temp)
        comp.seenCard(temp)

    # create discard pile and puts top card from deck in it
    discardPile = deck.Deck()
    temp = drawDeck.takeCard()
    discardPile.addCard(temp)
    comp.seenCard(temp)

    #alternate turns
    while knock == 0:
        # PLAYER 1 TURN
        print("IT IS P1 TURN\n")
        
        playerHand.printHand('player')
        
        print("\nThe top card of the discard pile is the:")
        discardPile.topCard().printCard()
        
        print('\nWhat would you like to do?')
        print('   1. take card from discard pile')
        print('   2. draw card from deck')
        print('   3. knock')
        move = input("(1, 2, or 3?)")
        while(move != '1' and move != '2' and move != '3'):
            print("INVALID RESPONSE")
            move = input("(1, 2, or 3?)")

            
        if move == '1': # take from discard
            temp = discardPile.takeCard()
            playerHand.addCard(temp)
            comp.addKnown(temp)

            print(' ')
            playerHand.printHand('player')

            print("\nWhich card would you like to discard?")
            dis = input("(1, 2, 3, or 4?)")
            while(dis != '1' and dis != '2' and dis != '3' and dis != '4'):
                print("INVALID RESPONSE")
                dis = input("(1, 2, 3, or 4?)")
                
            
            temp = playerHand.takeCard(int(dis)-1)
            discardPile.addCard(temp)
            comp.checkKnown(temp)
            comp.seenCard(temp)
            
        
        elif move == '2': # take from deck
            comp.addTurn()

            temp = drawDeck.takeCard()
            playerHand.addCard(temp)
            comp.seenCard(temp)

            print(' ')
            playerHand.printHand('player')

            print("\nWhich card would you like to discard?")
            dis = input("(1, 2, 3, or 4?)")
            while(dis != '1' and dis != '2' and dis != '3' and dis != '4'):
                print("INVALID RESPONSE")
                dis = input("(1, 2, 3, or 4?)")
            
            temp = playerHand.takeCard(int(dis)-1)
            discardPile.addCard(temp)
            comp.checkKnown(temp)
            comp.seenCard(temp)

            if drawDeck.cardsLeft() == 0:
                print("OUT OF CARDS! RESHUFFLING DISCARDS PILE")
                while discardPile.cardsLeft() != 0:
                    drawDeck.addCard(discardPile.takeCard())
                random.shuffle(drawDeck.cards)
                discardPile.addCard(drawDeck.takeCard())
                comp.reset(compHand, discardPile.topCard())
                
        
        else:  # knock
            knock = 1
            continue

        if knock != 0 or playerHand.getScore() == 31:
            continue

        # PLAYER 2 TURN
        print("IT IS P2 TURN\n")
        
        compHand.printHand('player')
        
        print("\nThe top card of the discard pile is the:")
        discardPile.topCard().printCard()
        
        print('\nWhat would you like to do?')
        print('   1. take card from discard pile')
        print('   2. draw card from deck')
        print('   3. knock')
        move = input("(1, 2, or 3?)")
        while(move != '1' and move != '2' and move != '3'):
            print("INVALID RESPONSE")
            move = input("(1, 2, or 3?)")

            
        if move == '1': # take from discard
            temp = discardPile.takeCard()
            compHand.addCard(temp)

            print(' ')
            compHand.printHand('player')

            print("\nWhich card would you like to discard?")
            dis = input("(1, 2, 3, or 4?)")
            while(dis != '1' and dis != '2' and dis != '3' and dis != '4'):
                print("INVALID RESPONSE")
                dis = input("(1, 2, 3, or 4?)")
                
            
            temp = compHand.takeCard(int(dis)-1)
            discardPile.addCard(temp)
            
        
        elif move == '2': # take from deck

            temp = drawDeck.takeCard()
            compHand.addCard(temp)

            print(' ')
            compHand.printHand('player')

            print("\nWhich card would you like to discard?")
            dis = input("(1, 2, 3, or 4?)")
            while(dis != '1' and dis != '2' and dis != '3' and dis != '4'):
                print("INVALID RESPONSE")
                dis = input("(1, 2, 3, or 4?)")
            
            temp = compHand.takeCard(int(dis)-1)
            discardPile.addCard(temp)
            

            if drawDeck.cardsLeft() == 0:
                print("OUT OF CARDS! RESHUFFLING DISCARDS PILE")
                while discardPile.cardsLeft() != 0:
                    drawDeck.addCard(discardPile.takeCard())
                random.shuffle(drawDeck.cards)
                discardPile.addCard(drawDeck.takeCard())
                
        
        else:  # knock
            knock = 1
            continue

        if knock != 0 or playerHand.getScore() == 31:
            continue
    
    
        print('////////////////////////////////////////////////////////////////')
        comp.known_player_hand.printHand("player")
        print(comp.prob(compHand.getScore()))
        print('////////////////////////////////////////////////////////////////')
        comp.record(playerHand, compHand)

    # print results
    print('\nEND OF GAME')
    playerHand.printHand('player')
    print('Score: ' + str(playerHand.getScore()) + '\n')
    compHand.printHand('compueter')
    print('Score: ' + str(compHand.getScore()) + '\n')


    # check hands
    if compHand.getScore() > playerHand.getScore():
        print('THE COMPUTER WINS!')
        return 0
    elif compHand.getScore() == playerHand.getScore():
        if knock == 1:
            print('THE COMPUTER WINS!')
            return 0

    print('YOU WIN!')
    return 1



# play game with one computer controled player and one random player to collect data
def playAgainstRandom(p):
    knock = 0

    #create computer player
    comp = computer.Computer()

    # create new deck
    drawDeck = deck.Deck()
    drawDeck.fillDeck()

    # deal 3 cards to each player
    playerHand = hand.Hand()
    compHand = hand.Hand()
    for i in range(3):
        playerHand.addCard(drawDeck.takeCard())
        temp = drawDeck.takeCard()
        compHand.addCard(temp)
        comp.seenCard(temp)

    # create discard pile and puts top card from deck in it
    discardPile = deck.Deck()
    temp = drawDeck.takeCard()
    discardPile.addCard(temp)
    comp.seenCard(temp)

    #alternate turns
    while knock == 0:
        
        # PLAYER 1 TURN
        print("IT IS P1 TURN\n")
        
        compHand.printHand('comp')
        playerHand.printHand('player')

        
        print("\nThe top card of the discard pile is the:")
        discardPile.topCard().printCard()
        
        print('\nWhat would you like to do?')
        print('   1. take card from discard pile')
        print('   2. draw card from deck')
        print('   3. knock')
        
        if(playerHand.getScore()/comp.draws < 7 and playerHand.getScore() < 25):
            move = random.randint(1,6)
        else:                                       #makes sure random opponent knocks somewhat conservatively
            move = random.randint(5,7)
        

            
        if move == 1 or move == 3 or move == 5: # take from discard
            print('PLAYER TOOK DISCARD')
            temp = discardPile.takeCard()
            playerHand.addCard(temp)
            comp.addKnown(temp)

            print(' ')
            playerHand.printHand('player')

            print("\nWhich card would you like to discard?")
            dis = random.randint(1,4)
            
                
            
            temp = playerHand.takeCard(int(dis)-1)
            discardPile.addCard(temp)
            comp.checkKnown(temp)
            comp.seenCard(temp)
            
        
        elif move == 2 or move == 4 or move == 6 : # take from deck
            print('PLAYER TOOK DECK')
            comp.addTurn()

            temp = drawDeck.takeCard()
            playerHand.addCard(temp)
            comp.seenCard(temp)

            print(' ')
            playerHand.printHand('player')

            print("\nWhich card would you like to discard?")
            dis = random.randint(1,4)
            
            
            temp = playerHand.takeCard(int(dis)-1)
            discardPile.addCard(temp)
            comp.checkKnown(temp)
            comp.seenCard(temp)

            if drawDeck.cardsLeft() == 0:
                print("OUT OF CARDS! RESHUFFLING DISCARDS PILE")
                while discardPile.cardsLeft() != 0:
                    drawDeck.addCard(discardPile.takeCard())
                random.shuffle(drawDeck.cards)
                discardPile.addCard(drawDeck.takeCard())
                comp.reset(compHand, discardPile.topCard())
                
        
        else:  # knock
            print('PLAYER KNOCKED   ---   ' + str(move))
            knock = 1
            continue


        if knock != 0 or playerHand.getScore() == 31:
            continue
        
        
        # COMPUTER TURN

        if(float(compHand.getScore())/float(comp.draws) > 12.0/(comp.draws**0.6) or comp.prob(compHand.getScore()) < 0.5 or compHand.getScore() > 27): #check if we should knock
            print("COMPUTER KNOCKED")
            knock = 2
            continue

        temp = compHand.getScore()
        compHand.addCard(discardPile.takeCard())
        check = comp.bestDiscard(compHand, "pile", temp)                  #check if flipped card helps hand
        discardPile.addCard(compHand.takeCard(check))
        if check != 3:
            print("COMPUTER TOOK FROM DISCARD PILE")
        else:
            print("COMPUTER TOOK FROM DREW A CARD FROM THE DECK")
            compHand.addCard(drawDeck.takeCard())
            check = comp.bestDiscard(compHand, "deck", temp)                      # draw from deck
            comp.seenCard(compHand.cards[check])
            discardPile.addCard(compHand.takeCard(check))

        if drawDeck.cardsLeft() == 0:
            print("OUT OF CARDS! RESHUFFLING DISCARDS PILE")
            while discardPile.cardsLeft() != 0:
                drawDeck.addCard(discardPile.takeCard())
            random.shuffle(drawDeck.cards)
            discardPile.addCard(drawDeck.takeCard())
            comp.reset(compHand, discardPile.topCard())

        if knock != 0 or playerHand.getScore() == 31:
            knock = 2
            continue
       



    
    # print results
    print('\nEND OF GAME')
    playerHand.printHand('player')
    print('Score: ' + str(playerHand.getScore()) + '\n')
    compHand.printHand('compueter')
    print('Score: ' + str(compHand.getScore()) + '\n')

    f = open("winData.txt", "a")
    # check hands
    if compHand.getScore() > playerHand.getScore():
        print('THE COMPUTER WINS!')
        f.write(str(compHand.getScore()) + ", " + str(playerHand.getScore()) + ", 1, " + str(knock) + ', ' + str(float(compHand.getScore())/float(comp.draws)) + ", " + str(comp.prob(compHand.getScore())) + "\n")
        f.close()
        return 0
    elif compHand.getScore() == playerHand.getScore():
        if knock == 1:
            print('THE COMPUTER WINS!')
            f.write(str(compHand.getScore()) + ", " + str(playerHand.getScore()) + ", 1, " + str(knock) + ', ' + str(float(compHand.getScore())/float(comp.draws)) + ", " + str(comp.prob(compHand.getScore())) + "\n")
            f.close()
            return 0

    print('YOU WIN!')
    f.write(str(compHand.getScore()) + ", " + str(playerHand.getScore()) + ", 0, " + str(knock) + ', ' + str(float(compHand.getScore())/float(comp.draws)) + ", " + str(comp.prob(compHand.getScore())) + "\n")
    f.close()
    return 1