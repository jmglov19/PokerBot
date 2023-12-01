from cards import *
from ScoreChecker import score_hand
import random
from Evaluation import eval_turn
# from AddjustedChatGTP import chat_gtp_turn
from EHSPlayer import EHS_decision

from tkinter import *
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from threading import Thread
import time


lock = threading.Lock()
global user_act



 
class CustomThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
 
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
             
    def join(self, *args):
        Thread.join(self)
        print("joined")
        return self._return


# This file of code will be what runs the actual game and will then have another
# file that will have the evaluation and what to do in a certain situation.

# Code used to simulate a game of poker
def simulate_game():
    print("new game")
    # Each player starts with 0 chips
    players = [0, 0]
    rounds = 0
    cur_turn = 0
    # While both players have more than 0 chips continue playing the game
    while rounds <= 20:
        print(rounds)
        print(players)
        winnings_label["text"] = "Winnings: " + str(players[1])
        opponents_action_label["text"] = "waiting"
        winner = play_poker(players, cur_turn)
        if cur_turn == 1:
            cur_turn = 0
        else:
            cur_turn = 1
        print(winner)

        # Thus code takes chips away from the loser and gives it to the winner
        if winner[0] == 0:
            #print("Winner is 0")
            #print(players)
            players[0] += winner[1]
            #print(players)
            #players[1] -= winner[1] // 2
        if winner[0] == 1:
            #print("Winner is 1")
            #print(players)
            players[1] += winner[1]
            #print(players)
            #players[0] -= winner[1] // 2
        if winner[0] == 2:
            players[0] += winner[1] // 2
            players[1] += winner[1] // 2
        rounds += 1

    if players[0] > players[1]:
        return 0
    if players[0] < players[1]:
        return 1
    return 2


# The betting turn is used in ever round of poker
def new_betting_turn(players, player_hands, community, pot, current_turn, round_num):
    # Set variables to zero before any turns
    zero_action = one_action = "Empty"
    zero_prev = one_prev = "Empty"
    cur_bet = 0
    fold = False

    # Go through this loop until someone calls or folds
    while True:
        #print("Turn Switch")
        #print(cur_bet)
        # Depending on whose turn it is pick an action
        if current_turn == 0:
            print("EHS")
            # Depending on the action we put take money from the player and put it into the pot
            zero_action = EHS_decision(pot, cur_bet, player_hands[0], community, round_num)
            #zero_action = random_turn(cur_bet)
            opponents_action_label["text"] = zero_action

            # If a player low raises and then is up raised they only have to put another 15 in.
            if zero_prev == "Low Raise" and (zero_action == "Call" or zero_action == "High Raise"):
                players[0] -= 15
                pot += 15
            elif zero_action == "High Raise":
                players[0] -= 30
                pot += 30
                cur_bet = 30
            elif zero_action == "Low Raise":
                players[0] -= 15
                pot += 15
                cur_bet = 15
            elif zero_action == "Call":
                players[0] -= cur_bet
                pot += cur_bet
            zero_prev = zero_action
            current_turn = 1
            #print(zero_action)
        elif current_turn == 1:
            #print("Eval")
            #one_action = random_turn(cur_bet)
            #one_action = eval_turn(cur_bet, pot, player_hands[1] + community, round_num)
            #one_action = userPlayer(player_hands[1], community, pot, cur_bet)
            #print("pt")
            user_thread = CustomThread(target=user, args=(player_hands[1], community, pot, cur_bet,))
            user_thread.start()
            one_action = user_thread.join()
            #print(one_action)
            if one_prev == "Low Raise" and (one_action == "Call" or one_action == "High Raise"):
                players[1] -= 15
                pot += 15
            elif one_action == "High Raise":
                players[1] -= 30
                pot += 30
                cur_bet = 30
            elif one_action == "Low Raise":
                players[1] -= 15
                pot += 15
                cur_bet = 15
            elif one_action == "Call":
                players[1] -= cur_bet
                pot += cur_bet
            one_prev = one_action
            #print(one_action)
            current_turn = 0

        # If one of these actions is taken, do one of the following
        # Break out of the loop if there is a fold, call or 2 checks
        if zero_action == "Fold" or one_action == "Fold":
            fold = True
            break
        # if one_action == "High Raise" or zero_action == "High Raise":
            # cur_bet = 30
        # if one_action == "Low Raise" or zero_action == "Low Raise":
            # cur_bet = 15
        if one_action == "High Raise" and zero_action == "High Raise":
            break
        if one_action == "Low Raise" and zero_action == "Low Raise":
            break
        if one_action == "Call" or zero_action == "Call":
            break
        if one_action == "Check" and zero_action == "Check":
            break

    # Calculate the new pot

    # Return the pot, who went last, and if there were any folds
    return pot, current_turn, fold


# This code is used for each game of poker
def play_poker(players, cur_turn):
    for widget in community_cards_frame.winfo_children():
        widget["image"] = unkwown_card
    # Create a new shuffled deck
    deck = create_deck()
    community = []
    # anti into the pot
    players[0] -= 5
    players[1] -= 5
    cur_pot = 10


    players_hands = deal_hands(2, deck)
    user_hand = players_hands[1]
    
    user_card0 = card_resize(user_hand[0])
    my_card_0["image"] = user_card0

    user_card1 = card_resize(user_hand[1])
    my_card_1["image"] = user_card1



    # Betting Turn

    # Each stage of poker is played in here
    for stage in range(4):
        #print(stage)
        #print(community)
        result = new_betting_turn(players, players_hands, community, cur_pot, cur_turn, stage)
        cur_pot = result[0]
        # result[2] is the fold condition
        # If this is triggered we exit the game and give the pot to the winner
        if result[2]:
            if result[1] == 1:
                return 1, cur_pot
            elif result[1] == 0:
                return 0, cur_pot
        # Get the new pot after the folds, so we don't have players losing money they didn't bet
        #cur_pot = result[0]
        # If it is round 0 we need to draw 3 community cards for the next round
        if stage == 0:
            for i in range(3):
                community.append(deck.pop())
                
            community_card0 = card_resize(community[0])
            community_card_1["image"] = community_card0

            community_card1 = card_resize(community[1])
            community_card_2["image"] = community_card1

            community_card2 = card_resize(community[2])
            community_card_3["image"] = community_card2   
        # Otherwise we need to jst draw one for the turn and the river
        else:
            community.append(deck.pop())
            if stage == 1:
                community_card3 = card_resize(community[3])
                community_card_4["image"] = community_card3 
            if stage == 2:
                community_card4 = card_resize(community[4])
                community_card_5["image"] = community_card4 

        cur_turn = result[1]


    # This code is used for if the game reaches the final stage and we need to compare the 2 best hands and decide a
    # winner
    player_scores = []
    for player in players_hands:
        player_scores.append(score_hand(player + community))
    #print(player_scores)

    # If we have a tie return a 2 so that nothing happes
    if player_scores[0] == player_scores[1]:
        return 2, cur_pot

    # Returns for a player who won the game
    elif player_scores[0] > player_scores[1]:
        return 0, cur_pot
    elif player_scores[1] > player_scores[0]:
        return 1, cur_pot


# This code is used for when we want to enter a player who plays randomly
def random_turn(cur_bet):
    if cur_bet > 0:
        return "Call"

    move = random.random()
    if move > 0.6:
        return "Check"
    elif move > 0.1:
        return "Raise High"
    else:
        return "Fold"


def userPlayer(ourcards, communityCards, pot, current_bet):
    print(ourcards, communityCards, current_bet, pot)
    action = input("What would you like to do?")
    return action


def play():
    game_thread = Thread(target=simulate_game)
    game_thread.start()


def user(ourcards, communityCards, current_bet, pot):
    ev = threading.Event()
    print("player turn")
    print(ourcards, communityCards, current_bet, pot)

    for card in ourcards:
        print(card_resize(card))
    global user_act
    user_act = "wait"

    def check():
        print("new thread")
        while user_act == "wait":
            time.sleep(0.1)
            #print(user_act)
        lock.acquire()
    
        print("got lock")
        print(user_act)
        lock.release()
        ev.set()
        

    
    thrd1 = Thread(target=check)
    thrd1.start()
    #print("waiting")
    ev.wait()
    #print("moving on")
    thrd1.join
    print(user_act)
    return user_act
    
    
             
    

def call():
    print(1)
    global user_act
    user_act = "Call"
    


def check():
    print(1)
    global user_act
    user_act = "Check"
    

def fold():
    print(1)
    global user_act
    user_act= "Fold"
    

def high_raise():
    print(1)
    global user_act
    user_act= "High Raise"
    

def low_raise():
    print(1)
    global user_act
    user_act = "Low Raise"


def card_resize(card):
    if card[0] > 10:
        if card[0] == 11:
            address = "jack_of_" + card[1] +"2.png"
        if card[0] == 12:
            address ="queen_of_" + card[1] +"2.png"
        if card[0] == 13:
            address = "king_of_" + card[1] +"2.png"
        if card[0] == 14:
            address = "ace_of_" + card[1] +".png"
    else:
        address = str(card[0]) + "_of_" + card[1] + ".png"
    
    address = "cards/" + address
    img = Image.open(address)
    img_resize = img.resize((125,200))
    return ImageTk.PhotoImage(img_resize)
        


    


root = tkinter.Tk()
root.title("Poker Bot")



button_start = Button(root, text="Deal Hand", command=play)
button_start.grid(row=0, column=0)
winnings_label = Label(root, text= "Winnings: 0")
winnings_label.grid(row= 0, column= 1)
opponents_action_label = Label(root, text= "Waiting")
opponents_action_label.grid(row=0, column=2)


my_cards_frame = tkinter.LabelFrame(root, text= "My Cards")
my_cards_frame.grid(row=1, column=0)



unknown_img = Image.open("cards/unknown.png")
my_img = unknown_img.resize((125,200))
unkwown_card= ImageTk.PhotoImage(my_img)



my_card_0 = Label(my_cards_frame, image=unkwown_card)
my_card_0.grid(row=0, column=0)

my_card_1 = Label(my_cards_frame, image=unkwown_card)
my_card_1.grid(row=0, column=1)


community_cards_frame = tkinter.LabelFrame(root, text= "Community Cards")
community_cards_frame.grid(row=2, column=0)


#Community Cards
community_card_1 = Label(community_cards_frame, image=unkwown_card)
community_card_1.grid(row=0, column=0)

community_card_2 = Label(community_cards_frame, image=unkwown_card)
community_card_2.grid(row=0, column=1)

community_card_3 = Label(community_cards_frame, image=unkwown_card)
community_card_3.grid(row=0, column=2)

community_card_4 = Label(community_cards_frame, image=unkwown_card)
community_card_4.grid(row=0, column=3)

community_card_5 = Label(community_cards_frame, image=unkwown_card)
community_card_5.grid(row=0, column=4)



actions_frame = tkinter.LabelFrame(root, text= "Actions")
actions_frame.grid(row=3, column=0)

# Low Rase, High Raise, Call, Check, Fold

check_button = Button(actions_frame, text="Check", command=check)
check_button.grid(row=0, column=0)

call_button = Button(actions_frame, text="Call", command=call)
call_button.grid(row=0, column=1)

fold_button = Button(actions_frame, text="Fold", command=fold)
fold_button.grid(row=0, column=2)

high_raise_button = Button(actions_frame, text="High Raise", command=high_raise)
high_raise_button.grid(row=0, column=3)

low_raise_button = Button(actions_frame, text="Low Raise", command=low_raise)
low_raise_button.grid(row=0, column=4)
#
#my_img = ImageTk.PhotoImage(Image.open("cards/3_of_clubs.png"))
#my_label = Label(image=my_img)
#my_label.pack()

button_quit =Button(root, text= "Exit", command=root.quit)
button_quit.grid(row=4, column=0)

root.mainloop()


