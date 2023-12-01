import threading
from threading import Thread
import time

global action

lock = threading.Lock()

def first(lock):
    global action
    action = "wait"
    
    while action == "wait":
        print("waiting")
    lock.acquire()
    print("first is in")
    print(action)
    time.sleep(1)
    print("first is out")
    lock.release()

def second(lock):
    global action
    
    
    lock.acquire()

    
    print("second is in")
    print(action)
    action = "move"
    print(action)
    time.sleep(1)
    print("second is out")
    lock.release()

thrd1 = Thread(target=first, args=(lock,))
thrd2 = Thread(target=second, args=(lock,))

thrd1.start()
thrd2.start()

thrd1.join()
thrd2.join()