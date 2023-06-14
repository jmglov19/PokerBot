# Implementation of the ehs algorithm
import time
from ScoreChecker import score_hand
import itertools


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), round(sec)))


def create_deck():
    numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    deck = []
    for i in suits:
        for j in numbers:
            deck.append((j, i))
    return deck


def HandStrength(ourcards, boardcards):
    ahead = tied = behind = 0
    ourrank = score_hand(ourcards + boardcards)

    deck = create_deck()
    for our_card in ourcards:
        deck.remove(our_card)
    for board_card in boardcards:
        deck.remove(board_card)

    com_set = itertools.combinations(deck, 2)

    for oppcards in com_set:
        # print(oppcards)

        opprank = score_hand(list(oppcards) + boardcards)
        if (ourrank > opprank):
            ahead += 1
        elif (ourrank == opprank):
            tied += 1
        else:
            behind += 1

    handstrength = (ahead + tied / 2) / (ahead + tied + behind)

    return handstrength


def HandPotential(ourcards, boardcards):
    ahead = 0
    tied = 1
    behind = 2
    # Hand potential array, each index represents ahead, tied, and behind
    hp = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]
    hp_total = [0, 0, 0]  # initialize to 0
    ourrank = score_hand(ourcards + boardcards)

    # Consider all two card combinations of the remaining cards for the opponent
    deck = create_deck()
    for our_card in ourcards:
        deck.remove(our_card)
    for board_card in boardcards:
        deck.remove(board_card)

    oppcards = itertools.combinations(deck, 2)
    for opp_card in oppcards:

        opprank = score_hand(list(opp_card) + boardcards)
        if ourrank > opprank:
            index = ahead
        elif ourrank == opprank:
            index = tied
        else:
            index = behind

        # hp_total[index] += 1

        # All possible board cards to come
        temp_deck = deck.copy()
        for card in list(opp_card):
            temp_deck.remove(card)

        turn_river = itertools.combinations(temp_deck, 5 - len(boardcards))

        for case in turn_river:
            # Final 5-card board
            board = boardcards + list(case)
            ourbest = score_hand(ourcards + board)
            oppbest = score_hand(list(opp_card) + board)
            if ourbest > oppbest:
                hp[index][ahead] += 1
            elif ourbest == oppbest:
                hp[index][tied] += 1
            else:
                hp[index][behind] += 1
            hp_total[index] += 1

    if (hp_total[behind] + hp_total[tied]) == 0:
        Ppot = (hp[behind][ahead] + hp[behind][tied] / 2 + hp[tied][ahead] / 2) / 1
        Npot = (hp[ahead][behind] + hp[tied][behind] / 2 + hp[ahead][tied] / 2) / 1

    else:
    # Ppot: were behind but moved ahead
        Ppot = (hp[behind][ahead] + hp[behind][tied] / 2 + hp[tied][ahead] / 2) / (hp_total[behind] + hp_total[tied])
    # Npot: were ahead but fell behind
    # Not going to calculate because it'll be too conservative and it is better to out bet opponents
        Npot = (hp[ahead][behind] + hp[tied][behind] / 2 + hp[ahead][tied] / 2) / (hp_total[ahead] + hp_total[tied])

    return Ppot, Npot


def EHS_score(OurCards, BoardCards):
    #StartTime = time.time()
    HS = HandStrength(OurCards, BoardCards)
    HP = HandPotential(OurCards, BoardCards)
    # EHS = (HS * (1 - HP[1])) + ((1 - HS) * HP[0])
    aggressive_EHS = HS + (1 - HS) * HP[0]
    #EndTime = time.time()
    #TimeLapsed = EndTime - StartTime
    #time_convert(TimeLapsed)
    return aggressive_EHS

# Current_Our_Cards = [(14, 'Hearts'), (14, 'Diamonds')]
# Current_Board_Cards = [(2, 'Hearts'), (4, 'Diamonds'), (2, 'Spades')]


# print(EHS_score(Current_Our_Cards, Current_Board_Cards))


# print(HandStrength([(13, 'Hearts'), (2, 'Diamonds')], [(4, 'Hearts'), (4, 'Diamonds'), (14, 'Spades')]))
# print(HandPotential([(13, 'Hearts'), (2, 'Diamonds')], [(4, 'Hearts'), (4, 'Diamonds'), (14, 'Spades')]))
