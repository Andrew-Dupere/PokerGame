#import random module to shuffle the deck

import random

#define global variables to call on when creating classes

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

#set a playing variable equal to true in order to use while loops to control the game

playing = True

class Card:
    
    #each card object takes in a suit and rank attribute
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    #add a string method that returns rank and suit when asked to print a card
    
    def __str__(self):
        return self.rank + " of "+ self.suit
    
class Deck:
    
    #To create the deck class start with an empty list, then
    #iterate through each suit and rank and append it to the list
    
    def __init__(self):
        self.deck = [] 
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
                
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+card.__str__()
        return "The deck has: "+deck_comp
    
    #create a shuffle method by randomizing the order of the deck list
    
    def shuffle(self):
        random.shuffle(self.deck)
        
    #create a deal method by using pop to remove the last item in the deck list
    #and have the popped item exist as a single_card variable for later use
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card
                
#start with an empty list to create a hand class
#create attributes to keep track of the value of a hand and to

class Hand:
    def __init__(self):
        self.cards = [] 
        self.value = 0
        self.aces = 0 
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        if card.rank == 'Ace':
            self.aces += 1
        
    #to adjust for aces check if the value of a hand is greater than 21 and if aces exist in the hand
    #then reduce the hand value by 10 (aces = 11 or 1) and the ace counter by 1
    
    def adjust_for_ace(self):
        
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
            
#A chip class keeps track of the player and dealer chips using counter variables
#self.total is set equal to the number of chips each player starts with

class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0
    def win_bet(self):
        self.total += self.bet
    def lose_bet(self):
        self.total -= self.bet
        
        
#create a take_bet function to ask the player how much they would like to bet
#use try and accept blocks to make sure the bet is an integer and the player has enough chips

def take_bet(chips):
    
    #use a while loop to continue prompting the player in the case of an invalid input
    
    while True:
        
        try:
            chips.bet = int(input("How much would you like to bet? "))
        except: 
            print("please use an integer")
        else:
            if chips.bet > chips.total:
                print('you only have {}'.format(chips.total))
            else:
                break
                
                
#define a hit function to take a card from the deck and add it to a players hand
#make sure to run the ace adjustment function

def hit(deck,hand):
    
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()
    
    
def hit_or_stand(deck,hand):
    
    #use a while loop again to continue hitting until the player wants to stand
    
    global playing
    
    while True:
        x = input('Hit or Stand? Enter h or s ')
        
        if x[0].lower() == 'h':
            hit(deck,hand)
            
        elif x[0].lower() == 's':
            print("Player Stands, Dealer's Turn")
            playing = False
            
        else: 
            print("Sorry, I do not understand")
            continue
        
        break    

#create two functions to show all or a partial amount of cards to the player

def show_some(player,dealer):

#show only 1 of the dealers cards, show all (2) of the players cards

    print("\n Dealer's Hand: ")
    print("Hidden Card")
    print(dealer.cards[1])
    print("\n Player Hand")
    for card in player.cards:
        print(card)


def show_all(player,dealer):
#show all dealer and player cards and display values

    print("\n Dealer's Hand")
    for card in dealer.cards:
        print(card)
    print(f"Dealer Value: {dealer.value}")

    print("\n Player Hand")
    for card in player.cards:
        print(card)
    print(f"Value of Player's Hand is: {player.value}")
          

#create a series of functions to account for all potential outcomes of each game
#then adjust the chips accordingly


def player_busts(player,dealer,chips):
    print("Player Busts")
    chips.lose_bet()
    
def player_wins(player,dealer,chips):
    print("Player Wins")
    chips.win_bet()
    
def dealer_busts(player,dealer,chips):
    print("Dealer Busts, Player Wins")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer Wins")
    chips.lose_bet()
    
def push(player,dealer):
    print("Push")
    
    
while True:
    
    print("Let the Games Begin!")
    
    #create the deck list and then shuffle the list
    
    deck = Deck()
    deck.shuffle()
    
    #create a hand for the dealer and the player
    #deal 2 cards to each 
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    #set up players chips
    
    player_chips = Chips()
    
    #ask player for their bet
    
    take_bet(player_chips)
    
    #use show_some to show the player's cards but keep the dealer's cards hidden
    
    show_some(player_hand,dealer_hand)
    
        
    while playing:
        
        #Ask player to hit or stand now that they have a hand and placed a bet
                
        hit_or_stand(deck,player_hand)
        
        #show some to keep one dealer card hidden
        
        show_some(player_hand,dealer_hand)
        
        #if the player hand exceeds 21 break out of the loop and run player busts
        
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            
        
            break
            
    #if player does not bust, dealer keeps hitting until their hand is exceeds 17
    
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
            
        #when player and dealer are done hitting, show all cards
            
        show_all(player_hand,dealer_hand)
        
        #run through potential outcomes of the game
        
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
            
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
        
        #tell the player how many chips they have left and ask if they want to continue
        
        print(f'\n Player has {player_chips.total} chips')
        
        
        new_game = input("Would you like to play again? y/n")
        
        if new_game[0].lower() == 'y':
            playing = True
            continue
        else:
            print("Game Over")
            break 
