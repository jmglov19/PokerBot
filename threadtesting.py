from threading import Thread

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
    
def add(n1, n2):
    result = n1 + n2
    return result
    
    
thread = CustomThread(target = add, args = (5, 4))
thread.start()
print(thread.join())