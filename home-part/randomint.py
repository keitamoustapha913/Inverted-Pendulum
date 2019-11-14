'''
14 Nov 2019 by Keita Mouhamed Moustapha
Implementation of lorentz using random.randint variables 
'''

import random
import time
import concurrent.futures
import os
import multiprocessing
import sys


# print(random.randint(1,100))
LorenzCOM = []
LorenzSerial = [0,1,2,3,4,5,6,7,8,9]
Sensor_values = [10,11,12,13,14,15,16,17,18,19]

def process_send_rand(i,a):
    # info('\n Process')
    dec_value = i
    index = LorenzSerial.index(i)
    # dec_value = random.randint(LorenzSerial,1000)
    # print(f'dec_value = {dec_value}')
    # Sensor_values[index] = dec_value
    Sensor_values.insert(index,dec_value)
    # print('\n Sensor_values  = ',Sensor_values)
    return dec_value

# To show the individual process IDs involved, here is an expanded example
def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def caller(func, args):
    result = func(*args)
    return result

def callerstar(args):
    return caller(*args)

# Testing the way to order a pool process
def test_ordered_pool():
    with multiprocessing.Pool(4) as pool:
        #
        # Tests
        #
        TASKS = [(process_send_rand, (i, 7)) for i in LorenzSerial]
        t1 = time.perf_counter()
        results = [pool.apply_async(caller, t) for t in TASKS]
        t2 = time.perf_counter()
        imap_it = pool.imap(callerstar, TASKS)
        t3 = time.perf_counter()
        imap_unordered_it = pool.imap_unordered(callerstar, TASKS)
        t4 = time.perf_counter()

        print('Ordered results using pool.apply_async():')
        for r in results:
            print('\t', r.get())
        print(f'with pool.apply_async Finished in {t2-t1} seconds')
        print()
        
        print('Ordered results using pool.imap():')
        for x in imap_it:
            print('\t', x)
        print(f'with pool.imap Finished in {t3-t2} seconds')
        print()

        print('Unordered results using pool.imap_unordered():')
        for x in imap_unordered_it:
            print('\t', x)
        print(f'with pool.imap_unordered Finished in {t4-t3} seconds')
        print()

        print('Ordered results using pool.map() --- will block till complete:')
        for x in pool.map(callerstar, TASKS):
            print('\t', x)
        print()




if __name__ == "__main__":
    
    # info('Main line')
    # print ('\t Sensor  = ',Sensor_values)

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     # results = [executor.submit(process_send_rand, i ) for i in LorenzSerial ]
    #     executor.submit(process_send_rand , LorenzSerial,Sensor_values )
    
    # print ('\t Sensor  = ',Sensor_values)
    test_ordered_pool()
    # for f in concurrent.futures.as_completed(results):
    #     print(f.result())
        

