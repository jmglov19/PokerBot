# This code will be used to score a hand and will return the best 5 card hand out of 7 cards

# Royal Flush, Straight Flush, Four of a Kind, Full House, Flush, Straight, 3 of kind, 2 pair, 1 pair
from itertools import combinations


# Takes the full 7 card hand and looks for the best 5 card hand it can create
def score_hand(full_hand):
    scores = []
    # creates all possible 5 card combinations
    hands = combinations(full_hand, 5)
    for hand in hands:
        sorted_hand = list(hand)
        sorted_hand.sort()

        # Check if there is a straight
        straight = check_straight(sorted_hand)
        # Check if all cards are the same suit
        flush = check_flush(sorted_hand)
        # Get the best score based on the numbers on the card
        kinds = check_kinds(sorted_hand)

        # Royal Flush
        if straight and flush and sorted_hand[4][0] == 14:
            scores.append((9, 0, 0, 0, 14))
        # Straight Flush
        elif straight and flush:
            scores.append((8, 0, 0, 0, sorted_hand[4][0]))
        # Four of a Kind
        elif kinds[0] >= 1:
            scores.append((7, kinds[1], 0, 0, sorted_hand[4][0]))
        # Full House
        elif kinds[2] == 1 and kinds[4] == 1:
            scores.append((6, 0, kinds[3], kinds[5], sorted_hand[4][0]))
        # Flush
        elif flush:
            scores.append((5, 0, 0, 0, sorted_hand[4][0]))
        # Straight
        elif straight:
            scores.append((4, 0, 0, 0, sorted_hand[4][0]))
            # Three of a Kind
        elif kinds[2] == 1:
            scores.append((3, 0, kinds[3], 0, sorted_hand[4][0]))
        # Two Pairs
        elif kinds[4] == 2:
            scores.append((2, 0, 0, kinds[5], sorted_hand[4][0]))
        # One Pair
        elif kinds[4] == 1:
            scores.append((1, 0, 0, kinds[5], sorted_hand[4][0]))
        # High Card
        else:
            scores.append((0, 0, 0, 0, sorted_hand[4][0]))
    
    return max(scores)


# Check for a royal fush, the best hand in the game
def check_royal_flush(hand):
    # if the hand doesn't have an ace in it then it is not worth going through
    if hand[4][0] != 14:
        return False
    # See if the hand has a straight and a flush
    if check_straight(hand) and check_flush(hand):
        return True

    return False


# Check to see if all 5 cards are the same suit
def check_flush(hand):
    suit = hand[0][1]  # get the suit of the first card
    # If any card is not that suit return false, otherwise return true
    for card in hand:
        if card[1] != suit:
            return False
    return True


# Check to see if all 5 cards are in order
def check_straight(hand):
    previous_card = hand[0][0]  # Get the number of the first card
    # Go through cards 2-5
    for card in range(1, 5):
        # if the current card is one ahead of the previous, continue with the loop
        if hand[card][0] == previous_card + 1:
            previous_card = hand[card][0]
        else:
            # Otherwise return false
            return False
    return True


# Check for cards with the same number
def check_kinds(hand):
    consecutive_count = 1  # set consecutive count to 1 for readability
    kind2 = 0
    kind3 = 0
    kind4 = 0

    # These are the high cards for the pairs so that they can be compared
    high_kind2 = 0
    high_kind3 = 0
    high_kind4 = 0

    # Start on the second card
    for card in range(1, 5):
        # if the current card has the same number as the previous card,
        # increase the consecutive count
        if hand[card][0] == hand[card - 1][0]:
            consecutive_count += 1
        # Otherwise, use the consecutive count to establish the amount of like cards
        # and get the card number of the like cards by looking at the previous card
        else:
            if consecutive_count == 2:
                kind2 += 1
                high_kind2 = hand[card - 1][0]
            if consecutive_count == 3:
                kind3 += 1
                high_kind3 = hand[card - 1][0]
            if consecutive_count == 4:
                kind4 += 1
                high_kind4 = hand[card - 1][0]
            consecutive_count = 1
    # Used for looking at the very last card
    # If the consecutive count is still going at the final card return the score
    if consecutive_count == 2:
        kind2 += 1
        high_kind2 = hand[3][0]
    if consecutive_count == 3:
        kind3 += 1
        high_kind3 = hand[3][0]
    if consecutive_count == 4:
        kind4 += 1
        high_kind4 = hand[3][0]
    # Return the amount of like cards and the high card
    return kind4, high_kind4, kind3, high_kind3, kind2, high_kind2

print(score_hand(
    [(2, 'Hearts'), (2, 'Diamonds'), (4, 'Hearts'), (4, 'Hearts'), (6, 'Spades'), (6, 'Clubs'), (10, 'Hearts')]))
