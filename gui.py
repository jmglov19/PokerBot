from tkinter import *
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from threading import Thread
import time


lock = threading.Lock()
global action






    



def user():
    ev = threading.Event()
    global action
    action = "wait"

    
    

    
    #def check():
        #print("thread made")
        #while action == "wait":
            #time.sleep(0.1)
            #print("waiting")
        #lock.acquire()

        #print("got lock")
        #print(action)
        #lock.release()
        #ev.set()
        

    
    #thrd1 = Thread(target=check)
    #thrd1.start()
    
    #ev.wait()
    
    
    #thrd1.join
    #time.sleep(5)
    print(action)
    return action
    
             
    

def call():
    global action
    action = "Call"
    


def check():
    global action
    action = "Check"
    

def fold():
    global action
    action = "Fold"
    

def high_raise():
    global action
    action = "High Raise"
    

def low_raise():
    global action
    action = "Low Raise"
    



root = tkinter.Tk()
root.title("Poker Bot")


button_start = Button(root, text="Deal Hand", command=(user))
button_start.grid(row=0, column=0)

my_cards_frame = tkinter.LabelFrame(root, text= "My Cards")
my_cards_frame.grid(row=1, column=0)



unknown_img = Image.open("cards/unknown.png")
my_img = unknown_img.resize((125,200))
unkwown_card= ImageTk.PhotoImage(my_img)



my_card_1 = Label(my_cards_frame, image=unkwown_card)
my_card_1.grid(row=0, column=0)

my_card_2 = Label(my_cards_frame, image=unkwown_card)
my_card_2.grid(row=0, column=1)


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

