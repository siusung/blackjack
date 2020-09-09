"""
BlackJack
Started on 8/22/2020
Trying to get back into the groove of coding and build some confidence that I can make my own project!

Steps for tomorrow:
Create hit or pass mechanism and record the card values
Record card value of the dealer, 17 hit limit
"""

import random
import os
import sys

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace')

values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 1}


def main():

    while True:
        print("\nNew Game: BLACK JACK")
        input("\nenter to start: ")
        os.system('cls')

        player_name = str(input("Name your player: "))
        
        player = Player(player_name)
        dealer = Dealer()

        input("\nenter to continue: ")
        os.system('cls')
        
        win, winner = False, None
        
        round_number = 1
        player_bet = 0
        
        # game start
        while not win:
            game_deck = Deck()
            game_deck.shuffle()
        
            print(f"ROUND: {round_number}")


            print(f"\nYour current balance is: ${player.bankroll}")

            while True:
                try:
                    player_bet = float(input("\nEnter your bet: (at least $5) "))
                    if player.bet(player_bet) == -1:
                        continue
                except:
                    print("Bruh, at least gimme a number")
                    continue
                else:
                    print("Nice bet, bro")
                    break    
        

            print(f"\nYour new balance is: ${round(player.bankroll, 2)}")

            input("\nenter to continue: ")
            os.system('cls')

            # initializing the hands and dealing two cards
            player_hand = Hand()
            dealer_hand = Hand()

            player_hand.add_card(game_deck.deal_one())
            player_hand.add_card(game_deck.deal_one())

            dealer_hand.add_card(game_deck.deal_one())
            dealer_hand.add_card(game_deck.deal_one())

            # check for wins
            def win_check(hand_value):
                if hand_value == 21:
                    print("\nWhy you lucky sonofagun, BLACKJACK!\nBut hold on, we gotta check the Dealer's hand too: ")
                    print('\n')
                    print("Dealer's Hand: ")
                    print('\n')
                    print(dealer_hand.full_hand())
                    print('\n')
                    print(f"Total: {dealer_hand.check_value()}")
                if hand_value > dealer_hand.check_value(): 
                    return True, "player"
                elif hand_value == dealer_hand.check_value():
                    return True, "tie"
                elif hand_value < dealer_hand.check_value():
                    return True, "dealer"
                return False, None

            # check for soft hands
            def player_ace_check(hand):
                if "Ace of Spades" in hand.full_hand() or "Ace of Clubs" in hand.full_hand() or "Ace of Hearts" in hand.full_hand() or "Ace of Diamonds" in hand.full_hand():
                    choice = None
                    while choice not in ["1", "11"]:
                        choice = input("\nPLAYER SOFT HAND: want an Ace value of 1 or 11? [1/11]: ")
                    if choice == "1":
                        return 0
                    elif choice == "11":
                        return 10
                return 0

            def dealer_ace_check(hand):
                if "Ace of Spades" in hand.full_hand() or "Ace of Clubs" in hand.full_hand() or "Ace of Hearts" in hand.full_hand() or "Ace of Diamonds" in hand.full_hand():
                    print("\nDEALER SOFT HAND")
                    if dealer_hand.check_value() + 10 <= 21:
                        return 10
                return 0

                

            print(f"ROUND: {round_number}")

            # displaying player's hand
            print('\n')
            print(player_name + "'s Hand: ")
            print('\n')
            print(player_hand.full_hand())
            print('\n')

            player_hand_value = player_hand.check_value()
            og_player_hand_value = player_hand_value
            print(f"Total: {player_hand_value}")
            
            # displaying dealer's hand
            print('\n')
            print("Dealer's Hand: ")
            print('\n')
            print(dealer_hand.partial_hand(1))
            print('\n')
            print("Total: dunno yet")

            change_value = player_ace_check(player_hand)
            player_hand_value += change_value
            if player_hand_value != og_player_hand_value:
                print(f"\n{player_name}'s new hand value: {player_hand_value}")

            win, winner = win_check(player_hand_value)

            # win conditions
            if winner == "player":
                player.bankroll += 2.5 * player_bet + player_bet
                print(f"\n{player_name} wins Round {round_number}!\nBlackjack pays 3 to 2: your new balance is {player.bankroll}")
            elif winner == "dealer":
                player.bankroll -= player_bet
                print(f"\nDealer wins Round {round_number}!\nYou've lost your bet: your balance is {player.bankroll}")
            elif winner == "tie":
                player.bankroll += player_bet
                print(f"It's a tie!\nYou receive your bet: your balance is back to {player.bankroll}")

            if player.bankroll < 5:
                print(f"\nYour current balance is: ${player.bankroll}")
                print('\n')
                print(f"\nNot enough dough, bro ;(")
                print('\n')
                print("GAME OVER")
                break

            win, winner = False, None
            input("\nenter next round: ")
            os.system("cls")
            round_number += 1
            

        



        

        # asking to replay
        if not replay():
            break

def replay():
    choice = None
    while choice not in ["y", "n"]:
        choice = input("Play again? [y/n]: ").lower()
    if choice == "y":
        return True
    elif choice == "n":
        return False


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank.capitalize()]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop(0)


class Hand:
    def __init__(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def check_value(self):
        value = 0
        for card in self.hand:
            value += card.value

        return value
    
    def full_hand(self):
            return ('\n'.join([str(card) for card in self.hand]))

    def partial_hand(self, number_of_cards):
        for i in range(number_of_cards):
            return '\n'.join([str(self.hand[i]) for x in range(number_of_cards)]) + "\n" + '\n'.join(["Card Face Down" for x in range(len(self.hand)-number_of_cards)])


class Player:
    def __init__(self, name):
        self.win_status = None
        self.name = name
        self.bankroll = 100.00

    def bet(self, bet_amount):
        if bet_amount <= self.bankroll and bet_amount >= 5:
            self.bankroll -= bet_amount
            return bet_amount
        return -1


class Dealer:
    def __init__(self):
        self.win_status = None
        self.dealer_hand = Hand()


if __name__ == '__main__':
    main()