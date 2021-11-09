import multiprocessing as mp
import os
import random
from time import sleep

def connect(philosophers):
    
    print("\nConnecting all philosophers....\n")
    
    for i in range(len(philosophers)):
        for j in range(i + 1, len(philosophers)):
            i_r, i_w = os.pipe()
            j_r, j_w = os.pipe()

            philosophers[i].read_pipe.append(os.fdopen(j_r))
            philosophers[j].read_pipe.append(os.fdopen(i_r))

            philosophers[i].write_pipe.append(i_w)
            philosophers[j].write_pipe.append(j_w)

    for i in range (len(philosophers)):
        print(philosophers[i].write_pipe)


class Philosopher:

    def __init__(self, id) -> None:
        self.process = None
        self._id = id
        
        self.clock = 0

        self.response_queue = mp.Queue()
        self.queue = mp.Queue()

        self._read_pipe = list()
        self._write_pipe = list()

    @property
    def get_id(self):
        return self._id

    @property
    def read_pipe(self):
        return self._read_pipe

    @property
    def write_pipe(self):
        return self._write_pipe

    def create(self):
        self.process = mp.Process(target=self.eat_and_think, args=())
        self.process.start()
        #self.process.join()

    def eat_and_think(self):
        
        while True:
            self.think()
            self.eat()

    def think(self):

        print("\nPhilosopher {} thinking.....\n".format(self.get_id))
        sleep(random.randint(3,5))
        

    def eat(self):
        sleep(4)
        print("\nPhilosopher {} checking to see if forks are available...\n".format(self.get_id))
        self.request_fork()

    def request_fork(self):
        
        print("Requesting fork\n")
        request = (self.get_id, self.clock)
        self.queue.put(request)

        print("Pipe => ", self.write_pipe)

        for pipe in self.write_pipe:
            os.write(pipe, bytes(request, encoding="utf8"))
            print("\nPhilosopher {} sends request {}".format(self.get_id, request))
            #os.write(pipe, bytes(request, encoding="utf8"))

            #message_interpretation = self.message_to_interpretation(Philosopher.get_message_tuple(request))
            #print(f"[Filozof {self.identifier}] šalje:\t'{message_interpretation}'\n", end="")

    def get_response(self):
        pass


if __name__ == "__main__":

    print("\n\tCreating philosophers....\n")

    for i in range(5):
        philosophers = [Philosopher(i) for i in range(5)]
        philosophers[i].create()

    connect(philosophers)