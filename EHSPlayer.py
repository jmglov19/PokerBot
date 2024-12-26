from EHS import EHS_score, HandStrength

optimalValueCoeff = 2

extreme = 64 - optimalValueCoeff
powerful = 60 - optimalValueCoeff
normal = 55 - optimalValueCoeff
weak = 50 - (optimalValueCoeff * 2)
awful = 43 - (optimalValueCoeff * 2)
lowerLimit = 40 - optimalValueCoeff


def EHS_decision(pot_size, cur_bet, our_cards, board_cards, stage):
   # pot_odds = pot_size / cur_bet

    # Pre_Flop
    if stage == 0:
        

        # Look at the array and see how powerful our 2 cards are
        # It would take way to long to run an ehs on this
        hand_value = pre_flop(our_cards)
        #print(our_cards)
        #print(hand_value)

        if hand_value >= powerful:
            return "High Raise"

        elif hand_value >= normal:
            if cur_bet == 0:
                return "Low Raise"
            else:
                return "Call"

        elif hand_value >= weak and cur_bet < 20:
            if cur_bet == 0:
                return "Check"
            return "Call"

        elif cur_bet == 0:
            return "Check"

        else:
            return "Fold"

    # Any other stages in the game we want to look at the ehs
    elif stage == 1:
        EHS = HandStrength(our_cards, board_cards)
        if cur_bet == 0:
            if EHS > 0.55:
                return "Low Raise"
            return "Check"
        else:
            if EHS > 0.7:
                return "High Raise"
            if EHS > 0.499:
                return "Call"
            else:
                return "Fold"

    else:
        EHS = EHS_score(our_cards, board_cards)

        if EHS > 0.7:
            return "High Raise"

        if cur_bet == 0:
            if EHS > 0.55:
                return "Low Raise"
            return "Check"
        if EHS > 0.499:
            return "Call"
        else:
            return "Fold"


# print(EHS_descion(50, 10,[(3, 'Clubs'), (4, 'Diamonds')],
# [(2, 'Diamonds'), (6, 'Diamonds'), (9, 'Diamonds'), (7, 'Diamonds')], 1))

starting_hand_scores = [
    [85, 67, 66, 65, 65, 63, 62, 61, 60, 60, 59, 58, 57],  # AA AKs AQs AJs ATs A9s A8s A7s A6s A5s A4s A3s A2s
    [65, 82, 63, 62, 62, 60, 59, 58, 57, 56, 55, 54, 53],  # AKo KK KQs KJs KTs K9s K8s K7s K6s K5s K4s K3s K2s
    [64, 61, 80, 60, 59, 58, 56, 54, 54, 53, 52, 51, 50],  # AQo KQo QQ QJs QTs Q9s Q8s Q7s Q6s Q5s Q4s Q3s Q2s
    [64, 61, 58, 78, 58, 56, 54, 52, 51, 50, 49, 48, 47],  # AJo KJo QJo JJ JTs J9s J8s J7s J6s J5s J4s J3s J2s
    [63, 60, 57, 55, 75, 54, 53, 51, 49, 47, 46, 46, 45],  # ATo KTo QTo JTo TT T9s T8s T7s T6s T5s T4s T3s T2s
    [61, 58, 56, 53, 52, 72, 51, 50, 48, 46, 44, 43, 42],  # A9o K9o Q9o J9o T9o 99 98s 97s 96s 95s 94s 93s 92s
    [60, 56, 54, 52, 50, 48, 69, 48, 47, 45, 43, 41, 40],  # A8o K8o Q8o J8o T8o 98o 88 87s 86s 85s 84s 83s 82s
    [59, 55, 52, 50, 48, 47, 46, 66, 48, 44, 42, 40, 38],  # A7o K7o Q7o J7o T7o 97o 87o 77 76s 75s 74s 73s 72s
    [58, 54, 51, 48, 46, 45, 44, 43, 63, 43, 41, 40, 38],  # A6o K6o Q6o J6o T6o 96o 86o 76o 66 65s 64s 63s 62s
    [58, 53, 50, 47, 44, 43, 42, 41, 40, 60, 41, 39, 38],  # A5o K5o Q5o J5o T5o 95o 85o 75o 65o 55 54s 53s 52s
    [56, 52, 49, 46, 43, 41, 40, 39, 38, 38, 57, 38, 36],  # A4o K4o Q4o J4o T4o 94o 84o 74o 64o 54o 44 43s 42s
    [56, 51, 48, 45, 42, 30, 38, 37, 36, 36, 34, 54, 35],  # A3o K3o Q3o J3o T3o 93o 83o 73o 63o 53o 43o 33 32s
    [55, 50, 47, 44, 41, 39, 37, 35, 34, 34, 33, 31, 50]  # A2o K2o Q2o J2o T2o 92o 82o 72o 62o 52o 42o 32o 22
]


def pre_flop(pre_flop_cards):
    pre_flop_cards.sort()
    card_one = pre_flop_cards[0]
    card_two = pre_flop_cards[1]
    suited = False
    if card_one[1] == card_two[1]:
        suited = True
    i = abs(card_one[0] - 14)
    j = abs(card_two[0] - 14)

    if suited:
        temp = i
        i = j
        j = temp
    return starting_hand_scores[i][j]


"""
    // if we are first to act on a small blind
    if (context.MoneyToCall == context.SmallBlind & & context.CurrentPot == context.SmallBlind * 3)
    {
    inPosition = true;

    if (handValue >= extreme)
    {
return PlayerAction.Raise(context.SmallBlind * 20);
}
else if (handValue >= powerful)
{
return PlayerAction.Raise(context.SmallBlind * 16);
}
else if (handValue >= normal)
{
return PlayerAction.Raise(context.SmallBlind * 12);
}
else if (handValue >= awful) // that makes around 74 % of all possible hands
{
// can
be
further
optimized
if (context.SmallBlind > context.MoneyLeft / 50)
    {
return PlayerAction.CheckOrCall();
}

return PlayerAction.Raise(context.SmallBlind * 10);
}
else if (handValue > lowerLimit & & context.SmallBlind < context.MoneyLeft / 40)
{
return PlayerAction.CheckOrCall();
}
else
{
return this.Fold();
}
}
else // we
are
on
big
blind or opp
has
raised
{
// opponent
has
not raised
if (context.MoneyToCall == 0)
{
if (handValue >= extreme) // cards like AA, KK, AKs
{
return PlayerAction.Raise(context.SmallBlind * 20);
}
else if (handValue >= powerful)
{
return PlayerAction.Raise(context.SmallBlind * 16);
}
else if (handValue >= awful) // that makes around 74 % of all possible hands
{
// can
be
further
optimized
if (context.SmallBlind > context.MoneyLeft / 50)
    {
return PlayerAction.CheckOrCall();
}

return PlayerAction.Raise(context.SmallBlind * 6);
}
else
{
return PlayerAction.CheckOrCall();
}
"""
