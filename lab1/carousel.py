import multiprocessing as mp
import queue
from random import randint
from time import sleep
from colorama import Fore

from numpy import random

class Carousel:

    def __init__(self) -> None:
        self.visitors = []
        self.process = None
        self.max_visitors = 4
        self.curr_visitors = 0
        self.curr_visitors_ids = []
        
        self.in_queue = mp.Queue()
        self.out_queue = mp.Queue()
        self.sync_queue = mp.Queue()

    def run(self):
        print("\n\t[CAROUSEL]: Creating visitors....\n")
        for i in range(8):
            self.visitors.append(Visitor(i))

        self.sync_queue.put(1)

        for i in range(0, len(self.visitors)):
            print(Fore.CYAN + "[CAROUSEL]: Visitor created with id => {}".format(self.visitors[i].get_id ))
            self.visitors[i].create_and_go(self.in_queue, self.out_queue, self.sync_queue)

        while self.visitors:
            msg, id = self.in_queue.get()
            self.curr_visitors_ids.append(id)
            print(Fore.WHITE + "\n\t[CAROUSEL]: Received msg => {}\n".format(msg))
            if msg == "I wanna ride":
                
                self.out_queue.put(("Sit down", id))
                self.curr_visitors += 1
                sleep(0.2)
                if self.curr_visitors == self.max_visitors:
                    
                    print(Fore.GREEN + "\n\t\t\t\t[CAROUSEL]: Carousel active now....\n")
                    sleep(random.randint(5,10))
                    print(Fore.RED + "\n\t\t\t\t[CAROUSEL]: Carousel stopped now!\n")
                    
                    for i in range(self.max_visitors):
                        self.out_queue.put(("Get up", self.curr_visitors_ids.pop()))
                    
                    self.curr_visitors = 0

            elif msg == "[VISITOR]: I am done":
                self.visitors.pop(id)




class Visitor:
    def __init__(self, id) -> None:
        self._id = id
        self.process = None

    @property
    def get_id(self):
        return self._id

    def create_and_go(self, input, output, sync):
        self.process = mp.Process(target=self.run, args=(input, output, sync))
        self.process.start()

    def run(self, queue_to_carousel : mp.Queue, queue_from_carousel : mp.Queue, sync_queue : mp.Queue):
        sleep(1)
        for _ in range(3):

            while True:
                sleep(random.randint(2, 3))
                sync_id = sync_queue.get()

                print(Fore.WHITE + "\nFROM SYNC ==> ", sync_id)
                print(Fore.WHITE + "\nVisitor ==> ", self.get_id)

                tmp = sync_id

                if tmp == 7: tmp = 0
                else: tmp += 1
                
                if sync_id == self.get_id:
                    
                    print(Fore.MAGENTA + "\n\t\t[VISITOR]: Visitor {} has the token!".format(self.get_id))
                    queue_to_carousel.put(("I wanna ride", self.get_id))

                    while True:
                            
                        cmd, id = queue_from_carousel.get()
                        sync_queue.put(tmp)
                        print("\n[VISITOR]: Token back in circulation\n")

                        if id == self.get_id:
                            print("\n\t[VISITOR]: Visitor {} sat down\n".format(self.get_id))
                            break
                        else:
                            queue_from_carousel.put((cmd, sync_id))
                            break

                    break

                else:
                    sleep(1)
                    sync_queue.put(sync_id)

            print("\n[VISITOR]: Visitor {} waiting to get up...\n".format(self.get_id))

            while True:
                sleep(random.randint(2, 3))
                sync_id = sync_queue.get()
                
                print(Fore.WHITE + "\nFROM SYNC ==> ", sync_id)
                print(Fore.WHITE + "\nVisitor ==> ", self.get_id)

                tmp = sync_id

                if tmp == 7: tmp = 0
                else: tmp += 1

                if sync_id == self.get_id:

                    print(Fore.MAGENTA + "\n\t\t[VISITOR]: Visitor {} has the token!".format(self.get_id))

                    while True:
                        
                        cmd, id = queue_from_carousel.get()
                        sync_queue.put(tmp)
                        print("\n[VISITOR]: Token back in circulation\n")

                        if id == self.get_id:
                            if cmd == "Get up":
                                print("\n\t[VISITOR]: Visitor {} got up and left the carousel\n".format(self.get_id))
                                break
                            else:
                                queue_from_carousel.put((cmd, sync_id))
                                break
                else:
                    sync_queue.put(sync_id)

        queue_to_carousel.put(("I am done", self.get_id))
        print("\n\t\t[VISITOR]: Visitor {} is done riding\n".format(self.get_id))



if __name__ == "__main__":

    carousel = Carousel()
    carousel.run()