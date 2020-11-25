#!/usr/bin/env python3

# This main file for the 31 card game player created by Cole Stevenson
# for assignment 4 of cmput 355 for the fall semester

import game, random

# itroduces the game and its rules
def intro():
    print("WELCOME TO THE CARD GAME 31!")
    rules = input("would you like me to go over the rules? (y or n)")
    if rules == 'y':
       f = open("rules.txt")
       print(f.read())
       f.close()
    play = input("ready to play? (y or n)")

    while(play != 'y' and play != 'test'):
        play = input("how about now?(y or n)")
    
    return play



def main():
    player_score = 0
    comp_score = 0
    go = intro()
    while go != 'n':
        if go == 'test':
            result = game.testPlay()
        else:
            result = game.play()

        if result == 1:
            player_score += 1
        else:
            comp_score +=1
        print("\nplayer: " + str(player_score))
        print("computer: " + str(comp_score) + "\n")
        go = input("Would you like to play again? (y or n)")

        while go != 'y' and go != 'n':
            print("INVALID RESPONSE")
            go = input("Would you like to play again? (y or n)")

    print("Thanks for Playing!")


# plays game between two random opponents to gather data
def randomPlay():
    for i in range(20):
        game.randomPlay(random.randint(20, 40))



# plays against random opponents at different knock sensitivities and records results
def playAgainstRandom():
   
    
    # p = 0.0

    # while p < 6:
        player_score = 0.0
        comp_score = 0.0
        for i in range(10000):
            result = game.playAgainstRandom(0)

            if result == 1:
                player_score += 1
            else:
                comp_score +=1
            print("\nplayer: " + str(player_score))
            print("computer: " + str(comp_score) + "\n")

        #f = open("trials.txt", 'a')
        # f.write(str(p) + ", " + str(comp_score/30.0) + "\n")
        # f.close()
        # p += 0.2
main()    
        

    
    




