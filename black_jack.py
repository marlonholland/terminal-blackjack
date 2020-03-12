import random

suits = ('Heart', 'Diamond', 'Spade', 'Club')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

#For printing these cards to the console, I'm using unicode symbols
symbols = {'Heart':'\u2665','Diamond':'\u2666', 'Spade':'\u2660', 'Club':'\u2663'}

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

        #values of the cards are only being used for printing to the console

        #numeric values
        if self.rank in ranks[0:9]:
            self.value = str(values[rank])
        #face values
        elif self.rank in ranks[9:13]:
            if self.rank == 'Jack':
                self.value = 'J'
            elif self.rank == 'Queen':
                self.value = 'Q'
            elif self.rank == 'King':
                self.value = 'K'
            elif self.rank == 'Ace':
                self.value = 'A'
    
    def __str__(self):
        symbol = symbols[self.suit]

        #10's are treated differently because they take two character spaces
        if self.value != '10':
            console_card = ' _____\n' +\
            f'|{symbol}   {symbol}|\n' +\
            '|     |\n' +\
            f'|  {self.value}  |\n' +\
            '|     |\n' +\
            f'|{symbol}   {symbol}|\n' +\
            ' ̅ ̅ ̅'
        else:
            console_card = ' _____\n' +\
            f'|{symbol}   {symbol}|\n' +\
            '|     |\n' +\
            f'| 1 0 |\n' +\
            '|     |\n' +\
            f'|{symbol}   {symbol}|\n' +\
            ' ̅ ̅ ̅'
        
        return console_card
    
    def __radd__(self, other):
        return other + str(self)
    
    def __add__(self, other):
        return str(self) + other
    
class Deck:

    def __init__(self):
        self.deck = []  
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_check = ''
        for card in self.deck:
            deck_check += str(card) + "\n"
        return 'DECK CHECK START-----------\n' + deck_check + 'DECK CHECK END-----------\n'
    
    def __radd__(self, other):
        return other + str(self)
    
    def __add__(self, other):
        return str(self) + other

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        top_card = self.deck.pop()
        return top_card

class Hand:

    def __init__(self):
        self.cards = []  
        self.value = 0   
        self.aces = 0   
    
    def add_card(self,card):
        if card.rank == 'Ace':
            self.aces += 1  
        self.cards.append(card)
        self.value += values[card.rank]
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
    
    def __str__(self):
        hand_check = ''
        for card in self.cards:
            hand_check += str(card) + "\n"
        return 'HAND CHECK START-----------\n' + hand_check + 'HAND CHECK END-----------\n'
    
    def __radd__(self, other):
        return other + str(self)

class Chips:
    
    def __init__(self):
        self.total = 100  
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


def take_bet(users_chips):
    while True:
        try:
            users_chips.bet = int(input('Please place your bet:  '))
            console_clear()
        except ValueError:
            console_clear()
            print('Please type an integer:  ')
            new_line()
        else:
            if users_chips.bet > users_chips.total:
                print (f"You can't bet that much. Your current balance is: {users_chips.total}")
                new_line()
            elif users_chips.bet <= 0:
                print ("You have to bet at least 1 chip!")
                new_line()
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    #Function will need to be able to control a while loop that sets the player's turn
    global player_turn
    while True:
        user_choice = input("Do you want to hit or stand? Type either 'hit' or 'stand':  ").lower()
        console_clear()
        if user_choice == 'hit':
            hit(deck, hand)
            break
        elif user_choice == 'stand':
            player_turn = False
            break
        else:
            console_clear()
            print("Invalid input. Please type 'hit' or 'stand':  ")
            new_line()

def show_some(player_hand,dealer_hand):
    #Player
    console_clear()
    print(f"Your hand value: {player_hand.value} \n")
    print("Your hand:")
    for card in player_hand.cards:
        print(card)
    print(' \n')
    #Dealer
    print(f"Dealer hand: \n{dealer_hand.cards[0]} \n")
    card_back = ' _____\n' +\
            '|     |\n' +\
            '|     |\n' +\
            '|     |\n' +\
            '|     |\n' +\
            '|     |\n' +\
            ' ̅ ̅ ̅'
    print(card_back)
    
def show_all(player,dealer):
        #Player
    print(f"Your hand value was: {player_hand.value} \n")
    print("Your hand was:")
    for card in player_hand.cards:
        print(card)
    print(' \n')
    #Dealer
    print(f"The dealer's hand value was: {dealer_hand.value} \n")
    print("Dealer's hand:")
    for card in dealer_hand.cards:
        print(card)
    print(' \n')

def player_busts(chips):
    print('You busted! \n')
    chips.lose_bet()

def player_wins(chips):
    print('You win! \n')
    chips.win_bet()

def dealer_busts(chips):
    print('Dealer busted! \n')
    chips.win_bet()
    
def dealer_wins(chips):
    print('Dealer wins! \n')
    chips.lose_bet()
    
def push():
    print("It's a tie! \n")


def play_again():
    while True:
        user_choice = input("Would you like to continue playing? Type either 'yes' or 'no':  ").lower()
        console_clear()
        if user_choice == 'yes' or user_choice == 'no':
            return user_choice
            break
        else:
            console_clear()
            print("Please type a valid input: 'yes' or 'no':  ")
            new_line()

def restart():
    while True:
        user_choice = input("You're out of chips!! Would you like to restart with 100 chips again? Type either 'yes' or 'no':  ")
        console_clear()
        if user_choice == 'yes' or user_choice == 'no':
            return user_choice
            break
        else:
            console_clear()
            print("Please type a valid input: 'yes' or 'no':  ")
            new_line()

def console_clear():
    print('\n'*100)

def new_line():
    print('\n')

def end():
    print('Thanks for playing!!')
    new_line()
    print(f'You ended the game with {chips.total} chips')

if __name__ == '__main__':

    while True:
        #Print opening statement
        console_clear()
        print('Welcome to Terminal Black Jack! A python script created by Marlon Holland :)')
        
        #Create hands 
        player_hand = Hand()
        dealer_hand = Hand()
        
        #If fresh game, or deck is low, create a new deck and shuffle it.
        try:
            deck
        except NameError:
            deck = Deck()
            deck.shuffle()
        else:
            if len(deck.deck) < 25:
                deck = Deck()
                deck.shuffle()        
        
        #Deal each player 2 cards
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())
        
        #If fresh game, set up player's chips (default 100)
        try:
            chips
        except NameError:
            chips = Chips()
            
        #Display chips and ask player for bet
        print('\n'*4)
        print(f'You have {chips.total} chips.')
        print('\n'*4)
        take_bet(chips)
        
        #After bet is taken, it is now the player's turn
        player_turn = True
        
        while player_turn:  
            
            #Show player their cards and dealer's first card
            show_some(player_hand, dealer_hand)
            
            #Ask player if they hit or stand(if player stands, player_turn is set to false)
            hit_or_stand(deck, player_hand)
    
            #If player's hand exceeds 21, player busts so no longer their turn
            if player_hand.value > 21:
                player_busts(chips)
                show_all(player_hand, dealer_hand)
                break
                
        #If player didn't bust and chooses to stand, play Dealer's hand until Dealer reaches 17
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)
            
            #Go through all the different winning scenarios and show the cards at the end
            if dealer_hand.value > 21:
                dealer_busts(chips)
                show_all(player_hand, dealer_hand)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(chips)
                show_all(player_hand, dealer_hand)
            elif player_hand.value > dealer_hand.value:
                player_wins(chips)
                show_all(player_hand, dealer_hand)
            elif player_hand.value == dealer_hand.value:
                push()
                show_all(player_hand, dealer_hand)

        #Inform player of their chips total, if out of chips ask if they want to restart
        if chips.total > 0:
            print(f'You now have {chips.total} chips.')
            new_line()
        else:
            restart_game = restart()
            if restart_game == 'yes':
                player_turn = True
                chips.total = 100
                continue
            elif restart_game == 'no':
                end()
                break

        #Ask if they want to play again
        game = play_again()
        if game == 'yes':
            player_turn = True
            continue
        elif game == 'no':
            end()
            break


