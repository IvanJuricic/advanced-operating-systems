import multiprocessing as mp
import queue
from time import sleep

from numpy import random

class Carousel:

    def __init__(self) -> None:
        self.visitors = []
        self.process = None
        self.max_visitors = 4
        self.curr_visitors = 0
        
        self.in_queue = mp.Queue()
        self.out_queue = mp.Queue()

    def run(self):
        print("\n\tCreating visitors....\n")
        for i in range(8):
            self.visitors.append(Visitor(i))

        for i in range(0, len(self.visitors)):
            print("Visitor created with id => {}".format(self.visitors[i].get_id ))
            self.visitors[i].create_and_go(self.in_queue, self.out_queue)

        while self.visitors:
            msg = self.in_queue.get()
            print("\n\tReceived msg => {}\n".format(msg))
            if msg == "I wanna ride":
                
                self.out_queue.put("Sit down")
                self.curr_visitors += 1
                sleep(0.2)
                if self.curr_visitors == self.max_visitors:
                    
                    print("\n\tCarousel active now....\n")
                    sleep(random.randint(5,10))
                    print("\n\tCarousel stopped now!\n")
                    
                    for i in range(4):
                        self.out_queue.put("Get up")
                    
                    self.curr_visitors = 0

            elif msg == "I am done":
                self.visitors.pop()



            


class Visitor:
    def __init__(self, id) -> None:
        self._id = id
        self.process = None

    @property
    def get_id(self):
        return self._id

    def create_and_go(self, input, output):
        self.process = mp.Process(target=self.run, args=(input, output))
        self.process.start()

    def run(self, queue_to_carousel : mp.Queue, queue_from_carousel : mp.Queue):
        sleep(1)
        for _ in range(3):
            
            sleep(random.randint(0.1, 1.5))
            queue_to_carousel.put("I wanna ride")

            while True:
                msg = queue_from_carousel.get()
                if msg != "Sit down":
                    queue_from_carousel.put(msg)
                else:
                    break

            print("\n\tVisitor {} sat down\n".format(self.get_id))

            while True:
                msg = queue_from_carousel.get()
                if msg != "Get up":
                    queue_from_carousel.put(msg)
                else:
                    break

            print("\n\tVisitor {} got up and left the carousel\n".format(self.get_id))

        queue_to_carousel.put("I am done")
        print("\n\t\tVisitor {} is done riding\n".format(self.get_id))



if __name__ == "__main__":

    carousel = Carousel()
    carousel.run()