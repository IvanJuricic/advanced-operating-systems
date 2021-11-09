import multiprocessing as mp
import queue
from random import randint
from time import sleep
from colorama import Fore

from numpy import random

class Carousel:

    def __init__(self) -> None:
        self.visitors = []
        self.max_visitors = 4
        self.curr_visitors = 0
        self.curr_visitors_ids = []
        
        self.in_queue = mp.Queue()
        
        self.out_sit_queue = mp.Queue()
        self.out_get_up_queue = mp.Queue()

        self.sync_queue = mp.Queue()

    def run(self):
        print("\n\t[CAROUSEL]: Creating visitors....\n")
        for i in range(8):
            self.visitors.append(Visitor(i))

        self.sync_queue.put(1)

        for i in range(0, len(self.visitors)):
            print(Fore.CYAN + "[CAROUSEL]: Visitor created with id => {}".format(self.visitors[i].get_id ))
            self.visitors[i].create_and_go(self.in_queue, self.out_sit_queue, self.out_get_up_queue, self.sync_queue)
            
        #sleep(1)
        
        while self.visitors:
            msg, id = self.in_queue.get()
            self.curr_visitors_ids.append(id)
            print(Fore.WHITE + "\n\t[CAROUSEL]: Received msg => {} from visitor {}\n".format(msg, id))
            if msg == "I wanna ride":
                
                self.out_sit_queue.put(("Sit down", id))
                self.curr_visitors += 1

                sleep(0.2)
                
                if self.curr_visitors == self.max_visitors:
                    
                    #Carousel.carousel_full = True
                    print("\n\t\t\t\t[CAROUSEL]: Visitor IDs that are on carousel => \n", self.curr_visitors_ids)
                    print(Fore.GREEN + "\n\t\t\t\t[CAROUSEL]: Carousel active now....\n")
                    sleep(random.randint(5,10))
                    print(Fore.RED + "\n\t\t\t\t[CAROUSEL]: Carousel stopped now!\n")
                    

                    for i in range(self.max_visitors):
                        #sleep(1)
                        #Carousel.visitors_sitting_down -= 1
                        id = self.curr_visitors_ids.pop()
                        self.out_get_up_queue.put(("Get up", id))
                    
                    self.curr_visitors = 0
                    #Visitor.carousel_full = False
                    

            elif msg == "I am done":
                self.curr_visitors_ids.pop()
                self.visitors.pop()




class Visitor:

    count = 0

    def __init__(self, id) -> None:
        self._id = id
        self.process = None
        self.waiting = False

    @property
    def get_id(self):
        return self._id

    def request_sit(self, queue_to_carousel : mp.Queue, queue_sit_from_carousel : mp.Queue, sync_queue : mp.Queue):
        
        queue_to_carousel.put(("I wanna ride", self.get_id))
        msg, id = queue_sit_from_carousel.get()
        
        #tmp = id
        #if tmp == 7: tmp = 0
        #else: tmp += 1

        print(Fore.LIGHTBLUE_EX + "\n[VISITOR]: Message from queue => {}\tID => {}".format(msg, id))

        if msg == "Sit down" and id == self.get_id:
            print(Fore.LIGHTYELLOW_EX + "\n[VISITOR]: Visitor {} sat down\n".format(self.get_id))
            self.count += 1
            self.waiting = True
            #sync_queue.put(tmp)

    def wait_get_up(self, queue_get_up_from_carousel : mp.Queue, sync_queue : mp.Queue):
        
        msg, id = queue_get_up_from_carousel.get()
        print(Fore.LIGHTBLUE_EX + "\n[VISITOR]: Message from queue => {}\tID => {}".format(msg, id))
        
        if msg == "Get up" and id == self.get_id:
            print("\n\t[VISITOR]: Visitor {} got up and left the carousel\n".format(self.get_id))
            self.waiting = False
            self.count -= 1
            #sync_queue.put(tmp)

    def create_and_go(self, input, output_sit, output_get_up, sync):
        self.process = mp.Process(target=self.run, args=(input, output_sit, output_get_up, sync))
        self.process.start()

    def run(self, queue_to_carousel : mp.Queue, queue_sit_from_carousel : mp.Queue, queue_get_up_from_carousel: mp.Queue, sync_queue : mp.Queue):
        
        sleep(1)

        for i in range(3):
            x = i + 1
            while True:
                sleep(randint(1,4))

                sync_id = sync_queue.get()

                tmp = sync_id
                if tmp == 7: tmp = 0
                else: tmp += 1

                if sync_id == self.get_id:
                    
                    self.request_sit(queue_to_carousel, queue_sit_from_carousel, sync_queue)
                    sync_queue.put(tmp)



                    if self.count == x:
                        self.wait_get_up(queue_get_up_from_carousel, sync_queue)
                        break

                else:
                    sync_queue.put(sync_id)
                

        queue_to_carousel.put(("I am done", self.get_id))
        print("\n\t\t[VISITOR]: Visitor {} is done riding\n".format(self.get_id))



if __name__ == "__main__":

    carousel = Carousel()
    carousel.run()