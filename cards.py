# This file will be used for making the cards and hands

from random import shuffle
#from ScoreChecker import score_hand


# Create New Deck
def create_deck():
    numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    suits = ['hearts', 'diamonds', 'clubs', 'spades']

    deck = []
    for i in suits:
        for j in numbers:
            deck.append((j, i))

    shuffle(deck)
    return deck


# Deal Hands to players
# n is the number of players, deck is the shuffled deck
def deal_hands(n, deck):
    players = []

    # Create a new player with an empty hand
    for player in range(n):
        players.append([])

    # for every player go in a circle handing 1 card to each player twice
    for p in range(n):
        for j in range(2):
            # Remove the card from the deck
            players[p].append(deck.pop())
    # Returns the players cards
    return players


# Check numbers
#print(score_hand(
    #[(10, 'Clubs'), (9, 'Diamonds'), (8, 'Hearts'), (7, 'Hearts'), (6, 'Hearts'), (5, 'Hearts'), (2, 'Hearts')]))
