from cards import *
from collections import Counter

card_values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13,
               "A": 14}
card_ranks = list(card_values.keys())


def translate_card(card):
    value = str(card[0])
    if value == "10":
        value = "T"
    if value == "11":
        value = "J"
    if value == "12":
        value = "Q"
    if value == "13":
        value = "K"
    if value == "14":
        value = "A"

    rank = card[1]
    rank = rank[0]
    return value + rank


def evaluate_action(hand, community_cards, round_num, min_bet, pot):
    tuple_of_cards = hand + community_cards
    for card in range(len(tuple_of_cards)):
        tuple_of_cards[card] = translate_card(tuple_of_cards[card])

    string_cards = ""

    for card in tuple_of_cards:
        string_cards += card
        string_cards += " "
    print(string_cards.split())

    # Combine the player's hand and the community cards
    all_cards = string_cards.split()

    # Evaluate the strength of the hand
    hand_score = evaluate_hand(all_cards)
    print(hand_score)

    # Determine the minimum bet to stay in the game
    # min_bet = bet

    # Determine the pot odds
    pot_odds = min_bet / (pot + min_bet)

    # pot_odds *= 1.2

    # Determine the recommended action based on the current round
    if round_num == 0:
        # Pre-flop round
        if hand_score >= 2:
            return "raise"
        elif hand_score >= 0:  # and pot_odds <= 0.2:
            return "call"
        else:
            return "fold"
    elif round_num == 1:
        # Flop round
        if hand_score >= 3:
            return "raise"
        elif hand_score >= 1 and pot_odds <= 0.2:
            return "call"
        else:
            return "fold"
    elif round_num == 2:
        # Turn round
        if hand_score >= 5:
            return "raise"
        elif hand_score >= 2 and pot_odds <= 0.2:
            return "call"
        else:
            return "fold"
    else:
        # River round
        if hand_score >= 6:
            return "raise"
        elif hand_score >= 3 and pot_odds <= 0.2:
            return "call"
        else:
            return "fold"


def evaluate_hand(hand):
    # Split hand into individual cards
    cards = hand

    # Count the frequency of each card rank
    card_counts = Counter([card[0] for card in cards])

    # Check for a straight
    straight = False
    for i in range(len(card_ranks) - 4):
        if all(rank in card_counts for rank in card_ranks[i:i + 5]):
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


def raise_pot():
    return 15


def chat_gtp_turn(cur_bet, cur_pot, round_num, hand, community):
    action = evaluate_action(hand, community, round_num, cur_bet, cur_pot)
    if action == "raise" and cur_bet >= 10:
        return -2
    if action == "raise":
        return raise_pot()
    if action == "fold":
        if cur_bet == 0:
            return -2
        return -1
    if action == "call":
        return -2


"""
print(translate_card((4, 'Diamonds')))

#player_hand = [(10, 'Clubs'), (11, 'Clubs'), (12, 'Clubs')]
#community = [(12, 'C'), (13, 'C'), (14, 'Clubs')]

tuple_of_cards = player_hand
for card in range(len(tuple_of_cards)):
    tuple_of_cards[card] = translate_card(tuple_of_cards[card])

    string_cards = ""

for card in tuple_of_cards:
    string_cards += card
    string_cards += " "
    print(string_cards.split())

    # Combine the player's hand and the community cards
all_cards = string_cards.split()


    # Evaluate the strength of the hand
hand_score = evaluate_hand(all_cards)


 #print(hand_score)
"""
