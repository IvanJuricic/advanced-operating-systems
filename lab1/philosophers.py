import multiprocessing as mp
import random
from time import sleep
from typing import List
from colorama import Fore
import numpy as np


class Philosopher:

    #forks = [0] * 5

    def __init__(self, id) -> None:
        self.process = None
        self._id = id
        
        self.clock = random.randint(1,1e4)

        self.queue = mp.Queue()
        #self._pipe = mp.Pipe()

    @property
    def get_id(self):
        return self._id

    @property
    def pipe(self):
        return self._pipe

    def eat_and_think(self, pipes):

        while True:
            self.think()
            self.eat(pipes)

    def think(self):

        print(Fore.LIGHTGREEN_EX + "\n\tPhilosopher {} thinking.....\n".format(self.get_id))
        sleep(2)
        

    def eat(self, pipes):
        #sleep(random.randint(2, 5))

        print(Fore.LIGHTYELLOW_EX + "\n\tPhilosopher {} checking to see if forks are available...\n".format(self.get_id))
        
        pipe = pipes[self.get_id][1]
        print("Pipe => ", pipe)
        sleep(np.random.uniform(0.2, 1.5))

        #self.send_request()

        #self.request_fork()
        #self.get_responses()
        #self.get_replies()
        
        #while True:
            #sleep(random.randint(1,3))
            #if self.check_critical_section() == True:
                #print(Fore.RED + "\n\t\tPhilosopher {} entered CS\n".format(self.get_id))
                #sleep(3)
                #break

    def check_critical_section(self):

        #print(Fore.MAGENTA + "All clocks from queue {} => ".format(self.get_id))
        self.sorted_queue.clear()
        while self.queue.qsize() != True: self.sorted_queue.append(self.queue.get())
        self.sorted_queue.sort()

        #print("lista => ", self.sorted_queue)
        
        id, clk = self.sorted_queue[0]
        print("Iz queuea ==> {} {}\n".format(id, clk))
        print("Iz klase ==> {} {}\n".format(self.get_id, self.clock))

        #sleep(random.randint(1,4))
            
        if id == self.get_id and clk == self.clock:
            print("***TRUE****")
            return True

        else:
            print("***FALSE***")
            for i in range(len(self.sorted_queue)):
                self.queue.put(self.sorted_queue[i])
            return False

    def send_request(self):
        
        #print("Requesting fork\n")
        request = (self.get_id, self.clock)
        self.queue.put(request)
        #print("\nNum of pipes for id {} {}".format(self.get_id, len(self.pipes)) )
        for pipe in self.pipes: pipe.send(request)

        #print(Fore.LIGHTBLUE_EX + "\n\tPhilosopher {} SENDING REQUEST {}!\n".format(self.get_id, request))

    def get_responses(self):
        for pipe in self.pipes:
            # Receive request
            id, clk = pipe.recv()
            #print(Fore.LIGHTGREEN_EX + "\n\tPhilosopher {} READING REQUEST {}!\n".format(self.get_id, (id, clk)))
            # Adjust logical clock
            self.clock = max(self.clock, clk) + 1
            # Add request to process queue
            self.queue.put((id, clk))
            # Send reply to requesting process
            if self.get_id > id: pipe.send((id, self.clock))
            else:
                x = self.get_id - 1 
                pipe.send((x, self.clock))
            #print(Fore.LIGHTYELLOW_EX + "\n\tPhilosopher {} REPLYING to {}!\n".format(self.get_id, id))

    def get_replies(self):
        for pipe in self.pipes:
            # Get reply
            id, clk = pipe.recv()
            #print(Fore.LIGHTGREEN_EX + "\n\tPhilosopher {} READING REPLY {}!\n".format(self.get_id, (id, clk)))
            # Add reply to process queue
            self.response_queue.put((id, clk))



class Table:

    def __init__(self) -> None:
       pass

    def create_philosophers(self, pipes, philosophers):
        print("\n\tCreating philosophers!\n")
        
        for i in range(5):
            philosophers[i] = Philosopher(i)

        self.connect(pipes)

        for i in range(len(philosophers)):
            p = mp.Process(target=philosophers[i].eat_and_think,args=(pipes,))
            p.start()
            p.join()

    def connect(self, pipes):
        
        print("\nConnecting all philosophers....\n")
        
        for i in range(len(philosophers)):
            #philosophers[i].pipe = mp.Pipe()
            pipes[i] = mp.Pipe()

        #print("\nNum of Connections => ", len(self.connections))
        #print("\nPhilosophers => ", philosophers[0].pipes)



if __name__ == "__main__":

    pipes = {}
    philosophers = {}

    table = Table()
    table.create_philosophers(pipes, philosophers)
