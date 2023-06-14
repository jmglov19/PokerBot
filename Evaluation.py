# Ths code is my own implementation of an evaluation algorithm of poker
# It looks at all the potential scores it could have and makes decisions on that
# The code also bluffs at certain points if it thinks that the other player is
# not confident about their hand.
import cards
import itertools
from AddjustedChatGTP import translate_card
from ScoreChecker import score_hand


def eval_turn(cur_bet, cur_pot, state, stage):
    # Pre_Flop
    if stage == 0 and cur_bet == 0:
        #print(state)
        # IF we have a pocket pair high raise
        if state[0][0] == state[1][0]:
            return "High Raise"
        # if we have two of the same suit low raise
        elif state[0][1] == state[1][1]:
            return "Low Raise"
        # If we have a good chance of a straight low raise
        elif abs(state[0][0] - state[1][0]) <= 4:
            return "Low Raise"
        else:
            # if no one hase went yet then check
            return "Check"

    # If there is a bet
    elif stage == 0:
        #print(state)
        # Pocket Pair
        if state[0][0] == state[1][0]:
            return "High Raise"
        # Same Suit
        elif state[0][1] == state[1][1]:
            return "Call"
        # Chance for a straight
        elif abs(state[0][0] - state[1][0]) <= 4:
            return "Call"
        # We have absolutely nothing
        else:
            return "Fold"

    # Everything past the pre-flop
    else:

        # Calculates our chances for different scores
        potent_scores = evaluation(state)
        translate_hand(state)
        # print(potent_scores)

        # This is a bluff mechanic. If the other player is not confident about their
        # hand and decides to check we put some pressure on them
        if cur_bet == 0 and stage >= 3:
            return "Low Raise"
        # if the current bet is low we will think about how good our hand is and
        # either out bet them or ust call
        if 5 <= cur_bet <= 20:
            for i in range(3, 10):
                if potent_scores[i] > 10.0 * stage:
                    return "High Raise"
            for i in range(3, 10):
                if potent_scores[i] > 2.0:
                    return "Call"

        # Looking at the potential scores we could have we could have,
        # if we have a large chance of having anything better than a 2 of a kind
        # We should raise high
        for i in range(3, 10):
            if potent_scores[i] > 12.0 * stage:
                return "High Raise"

        # if we have a low chance of getting anything we should
        # call or check
        for i in range(3, 10):
            if potent_scores[i] > 2.0:
                if cur_bet == 0:
                    return "Check"
                return "Call"

        # if There is a large pot we have already been in the game for a long time
        # and have a lot invested so let's just stay in any way
        if cur_pot > 100:
            if cur_bet == 0:
                return "Check"
            return "Call"

        # if the other player didn't bet anything, and we are not confident either
        # it is best to just check. No need to fold.
        if cur_bet == 0:
            return "Check"

        # Last case we fold
        else:
            return "Fold"


# This code is the evaluation of the potential scores
def evaluation(state):
    scores = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    # Create a new deck and remove the cards we already know
    deck = cards.create_deck()
    for card in state:
        deck.remove(card)
    # Generate all possible cards subtracted by the cards we already know
    com_set = itertools.combinations(deck, 7 - len(state))

    # increment the amount for every combination possible, so we can then
    # find the percentage chance of that outcome
    amount = 0

    for i in com_set:
        amount += 1
        scores[score_hand(state + list(i))[0]] += 1
    # Generate the percentages from the count
    for i in scores:
        scores[i] = round((scores[i] / amount) * 100, 2)
    #print(scores)
    # Return the potential scores
    return scores


# evaluation([(3, 'Clubs'), (4, 'Diamonds'), (2, 'Hearts'), (6, 'Diamonds'), (9, 'Hearts')], cards.create_deck())

# Used for translating cards so that they can be smaller to read and be compared with
# the chat gpt algorithm
def translate_hand(state):
    tuple_of_cards = state
    for card in range(len(tuple_of_cards)):
        tuple_of_cards[card] = translate_card(tuple_of_cards[card])

    string_cards = ""

    for card in tuple_of_cards:
        string_cards += card
        string_cards += " "
    # print(string_cards.split())


""" Test code for the evaluation
def test_eval(stateSize):
    deck = cards.create_deck()
    state = []
    for i in range(stateSize):
        state.append(deck.pop())
    #print(state)

    evaluation(state, deck)
"""
# test_eval(2)
# print(eval_turn(0, 10,[(3, 'Clubs'), (4, 'Diamonds')],0 ))
