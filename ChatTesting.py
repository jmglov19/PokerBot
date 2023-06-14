from collections import Counter

# Define card values and ranks
card_values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
card_ranks = list(card_values.keys())

def evaluate_hand(hand):
    # Split hand into individual cards
    cards = hand.split()

    # Count the frequency of each card rank
    card_counts = Counter([card[0] for card in cards])

    # Check for a straight
    straight = False
    for i in range(len(card_ranks) - 4):
        if all(rank in card_counts for rank in card_ranks[i:i+5]):
            straight = True
            break

    # Check for a flush
    flush = len(set([card[1] for card in cards])) == 1

    # Check for a straight flush
    straight_flush = straight and flush

    # Check for a royal flush
    royal_flush = straight_flush and card_ranks.index("T") in [card_values[card[0]] - 2 for card in cards]

    # Determine the highest card
    high_card = max(card_values[card[0]] for card in cards)

    # Check for a pair, two pairs, three of a kind, full house, and four of a kind
    pair = False
    two_pair = False
    three_of_a_kind = False
    full_house = False
    four_of_a_kind = False

    for count in card_counts.values():
        if count == 2:
            if pair:
                two_pair = True
            pair = True
        elif count == 3:
            three_of_a_kind = True
            if pair:
                full_house = True
        elif count == 4:
            four_of_a_kind = True

    # Determine the score
    if royal_flush:
        return 10
    elif straight_flush:
        return 9
    elif four_of_a_kind:
        return 8
    elif full_house:
        return 7
    elif flush:
        return 6
    elif straight:
        return 5
    elif three_of_a_kind:
        return 4
    elif two_pair:
        return 3
    elif pair:
        return 2
    else:
        return 1


hand1 = "AS KS QS JS TS" # Royal flush
hand2 = "9H 9D 9C 9S 4D" # Four of a kind
hand3 = "KS KH 2H 2S 2D" # Full house
hand4 = "3S 6S 8S QS AS" # Ace-high flush

print(hand1.split())


print(evaluate_hand(hand1))

