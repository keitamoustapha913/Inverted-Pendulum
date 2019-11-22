import multiprocessing
import time
import serial.tools.list_ports
import os
import sys
from multiprocessing import Pool


class polling_serial:

    def __init__(self, LorenzSerials):
        self.pool = Pool(4)
        self.LorenzSerials = LorenzSerials
        self.poll_start = [ 0x02, 0x5A, 0x01, 0xFF, 0x01, 0x01, 0x5C, 0xC7 ]
        self.poll_stop = [ 0x46 ]
        self.read_a = [ 0x41 ]
        self.read_b = [ 0x42 ]
        self.read_ab = [ 0x47 ]
        self.results = []
        self.numero = 0
        
        
    def caller(self,func, args):
        self.result = func(*args)
        return self.result

    def callerstar(self,args):
        return self.caller(*args)

    def process_send_rand(self,LorenzSerial,a):
        # t1 = time.perf_counter()
        LorenzSerial.open()
        LorenzSerial.write(self.poll_start)
        LorenzSerial.read(2)
        LorenzSerial.write(self.read_a)
        line = LorenzSerial.read(2)
        LorenzSerial.write(self.poll_stop)
        self.numero = int.from_bytes(line,  byteorder = 'big' ,signed= True)
        LorenzSerial.close()
        # t2 = time.perf_counter()
        # print(f'process_send_rand(self,LorenzSerial,a) Finished in {t2-t1} seconds \n')
        return self.numero

    # Testing the way to order a pool process
    def ordered_pool(self,core_number = 4):
        
        self.TASKS = [(self.process_send_rand, (LorenzSerial,0)) for LorenzSerial in self.LorenzSerials]
        # t1 = time.perf_counter()
        imap_it = self.pool.imap(self.callerstar, self.TASKS)
        # t2 = time.perf_counter()
        values = []
        # print('class Ordered results using pool.imap():')
        for x in imap_it:
            # print('\t', x)
            values.append(x)
        # print(f'class with pool.imap Finished in {t2-t1} seconds')
        # print()
        # return imap_it
        return values
        


    # https://stackoverflow.com/questions/25382455/python-notimplementederror-pool-objects-cannot-be-passed-between-processes
    '''
    __getstate__ is always called prior to pickling an object, and allow you to specify exactly which pieces of the object's state should actually be pickled. 
    Then upon unpickling, __setstate__(state) will be called if its implemented (it is in our case), or if it's not, the dict returned by __getstate__ will be used as the __dict__ for the unpickled instance. 
    In the above example, we're explicitly setting __dict__ to the dict we returned in __getstate__, but we could have just not implemented __setstate__ and gotten the same effect.
    '''
    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)

    # Testing the way to order a pool process
    def ordered_pools(self,core_number = 4):
        with multiprocessing.Pool(core_number) as pool:
            # t0 = time.perf_counter()
            self.TASKS = [(self.process_send_rand, (LorenzSerial,0)) for LorenzSerial in self.LorenzSerials]
            t1 = time.perf_counter()
            self.results = [pool.apply_async(self.caller, t) for t in self.TASKS]
            t2 = time.perf_counter()
            # imap_it = pool.imap(self.callerstar, self.TASKS)
            # t3 = time.perf_counter()
            # imap_unordered_it = pool.imap_unordered(self.callerstar, self.TASKS)
            # t4 = time.perf_counter()

            print('class Ordered results using pool.apply_async():')
            for r in self.results:
                print('\t', r.get())
            print(f'class with pool.apply_async Finished in {t2-t1} seconds')
            print()
            
            # print('class Ordered results using pool.imap():')
            # print('imap_it = ',imap_it)
            # for x in imap_it:
            #     print('\t', x)
            # print(f'class with pool.imap Finished in {t3-t2} seconds')
            # print()

            # print('class Unordered results using pool.imap_unordered():')
            # for x in imap_unordered_it:
            #     print('\t', x)
            # print(f'class with pool.imap_unordered Finished in {t4-t3} seconds')
            # print()

            # print('class Ordered results using pool.map() --- will block till complete:')
            # for x in pool.map(self.callerstar, self.TASKS):
            #     print('\t', x)
            # print()

            # a = t1-t0
            # b = t3 - t2
            # Total_time = b-a
            # print(f'class with pool.imap Final Finished in {Total_time} seconds')

        