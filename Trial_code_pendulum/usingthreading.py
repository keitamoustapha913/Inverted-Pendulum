'''
12 Nov 2019 by Keita Mouhamed Moustapha

using threading and time modules
'''
import serial.tools.list_ports
import time
import concurrent.futures
import os
import multiprocessing
import sys
import threading
from serialclass import polling_serial

# to write to file in background
from fileclass import AsyncWrite
# to handle the opc connection
from opcua import Client
from opcua import ua
from my_opc_class import Opc_Client

from random import randint

def get_ports():

    ports = serial.tools.list_ports.comports()
    
    return ports


def findLorenz(portsFound):
    
    commPort = 'None'
    numConnection = len(portsFound)
    
    for i in range(0,numConnection):
        port = foundPorts[i]
        #print("port", i , " = ", port, '\n')
        strPort = str(port)
        #print("strPort", i , " = ", strPort)
        
        if 'Lorenz' in strPort:
            splitPort = strPort.split(' ')
            #print("splitPort = ", splitPort)
            commPort = (splitPort[0])
            LorenzCOM.append(commPort)
            #print("commPort = ", commPort, '\n \n')
    #print( " Lorenz COM List = ", LorenzCOM)

    return commPort

# To create list of 4 Lorenz Serial objects
def createLorenzSerials(LorenzCOM):
    #print('Num of Lorenz = ',len(LorenzCOM) )
    
    if len(LorenzCOM) == 4:
        #print('All LorenzCOM connections detected ' )
        for i in range(len(LorenzCOM)):
            #LorenzSerials[i] = serial.Serial(port=LorenzCOM[i], baudrate=115200, timeout= 0.1)
            LorenzSerials.append( serial.Serial(port=LorenzCOM[i], baudrate=115200, timeout= 0.1) )
            #print( 'LorenzSerials',[i],' = ',LorenzSerials[i])
            LorenzSerials[i].close()
            #print( 'LorenzSerials',[i], 'closed')
        #print list of Lorenz's serial ports
        #print( 'LorenzSerials = ', LorenzSerials ) 
            
# To send command by Speed Optimized Polling Mode with threading
def Thread_send_polling(LorenzSerials):
    poll_start = [ 0x02, 0x5A, 0x01, 0xFF, 0x01, 0x01, 0x5C, 0xC7 ]
    poll_stop = [ 0x46 ]
    read_a = [ 0x41 ]
    read_b = [ 0x42 ]
    read_ab = [ 0x47 ]

    LorenzSerials.open()
    # print('Lorenz',LorenzSerials,' is opened')
    LorenzSerials.write(poll_start)
    emptyline = LorenzSerials.read(2)
    LorenzSerials.write(read_a)
    line = LorenzSerials.read(2)
    numero = int.from_bytes(line,  byteorder = 'big' )
    LorenzSerials.close()
    print ('\t numero  = ',numero)

# To send command by Speed Optimized Polling Mode with threading
def orderd_Thread_send_polling(lock,LorenzSerial):
    poll_start = [ 0x02, 0x5A, 0x01, 0xFF, 0x01, 0x01, 0x5C, 0xC7 ]
    poll_stop = [ 0x46 ]
    read_a = [ 0x41 ]
    read_b = [ 0x42 ]
    read_ab = [ 0x47 ]
    global x
    LorenzSerial.open()
    LorenzSerial.write(poll_start)
    emptyline = LorenzSerial.read(2)
    LorenzSerial.write(read_a)
    line = LorenzSerial.read(2)
    numero = int.from_bytes(line,  byteorder = 'big' )
    LorenzSerial.close()
    print ('\t numero  = ',numero)
    index = LorenzSerials.index(LorenzSerial)
    lock.acquire()
    x[index] = numero
    lock.release()

def ordered_threading():
    t5 = time.perf_counter() 
    for LorenzSerial in LorenzSerials:
        t1 = threading.Thread(target = orderd_Thread_send_polling, args = (lock,LorenzSerial))
        t1.start()
        t1.join()
    t6 = time.perf_counter()
    print(f'with threading.Lock Ordered Finished in {t6-t5} seconds')



# To send command by Speed Optimized Polling Mode without threading
def send_polling(LorenzSerials):
    poll_start = [ 0x02, 0x5A, 0x01, 0xFF, 0x01, 0x01, 0x5C, 0xC7 ]
    poll_stop = [ 0x46 ]
    read_a = [ 0x41 ]
    read_b = [ 0x42 ]
    read_ab = [ 0x47 ]

    t1 = time.perf_counter()
    # For each lorentz com send request a polling and close the serial
    for i in range(len(LorenzSerials)):
        LorenzSerials[i].open()
        # print('Lorenz',[i],' is opened')
        LorenzSerials[i].write(poll_start)
        emptyline = LorenzSerials[i].read(2)
        LorenzSerials[i].write(read_a)
        line = LorenzSerials[i].read(2)
        numero = int.from_bytes(line,  byteorder = 'big' )
        LorenzSerials[i].close()
        print ('\t numero',[i],' = ',numero)
    t2 = time.perf_counter()
    print(f'Without Threading Finished in {t2-t1} seconds')

def caller(func, args):
    result = func(*args)
    return result

def callerstar(args):
    return caller(*args)

def process_send_rand(LorenzSerial,a):
    poll_start = [ 0x02, 0x5A, 0x01, 0xFF, 0x01, 0x01, 0x5C, 0xC7 ]
    poll_stop = [ 0x46 ]
    read_a = [ 0x41 ]
    read_b = [ 0x42 ]
    read_ab = [ 0x47 ]

    LorenzSerial.open()
    LorenzSerial.write(poll_start)
    LorenzSerial.read(2)
    LorenzSerial.write(read_a)
    line = LorenzSerial.read(2)
    numero = int.from_bytes(line,  byteorder = 'big' )
    LorenzSerial.close()
    return numero

# Testing the way to order a pool process
def test_ordered_pool():
    with multiprocessing.Pool(4) as pool:
        #
        # Tests
        #
        TASKS = [(process_send_rand, (LorenzSerial,0)) for LorenzSerial in LorenzSerials]
        t1 = time.perf_counter()
        results = [pool.apply_async(caller, t) for t in TASKS]
        print(results)
        t2 = time.perf_counter()
        imap_it = pool.imap(callerstar, TASKS)
        t3 = time.perf_counter()
        imap_unordered_it = pool.imap_unordered(callerstar, TASKS)
        t4 = time.perf_counter()

        print('Ordered results using pool.apply_async():')
        t5 = time.perf_counter()
        for r in results:
            print('\t', r.get())
        t6 = time.perf_counter()
        print(f'with pool.apply_async Finished results in {t6-t5} seconds')
        print(f'with pool.apply_async Finished r.get in {t2-t1} seconds')
        print()
        
        print('Ordered results using pool.imap():')
        print('imap_it = ',imap_it)
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
        t7 = time.perf_counter()
        for x in pool.map(callerstar, TASKS):
            print('\t', x)
        print()
        t8 = time.perf_counter()
        print(f'Ordered results using pool.map() Finished in {t8-t7} seconds')


        
LorenzCOM = []
LorenzSerials = []
x = [1,1,1,1]
sensor_readings = []
message_log = ''

if __name__ == "__main__":

    
    foundPorts = get_ports()        
    connectPort = findLorenz(foundPorts)
    print( " Lorenz COM List = ", LorenzCOM)
    lock = threading.Lock()
    my_client = Opc_Client()
    

    if connectPort != 'None':
        createLorenzSerials(LorenzCOM)

        myserial_poll = polling_serial(LorenzSerials)
        t1 = time.perf_counter()
        for i in range(0, 2000 , 3):
            # t2 = time.perf_counter()
            sensor_readings = myserial_poll.ordered_pool(core_number = 4)
            # t7 = time.perf_counter()
            my_pressures_readings = my_client.collecting_pressures()
            # t3 = time.perf_counter()

            message = []
            for reading in sensor_readings:
                message.append(reading)

            for reading in my_pressures_readings:
                message.append(reading)
            
            t4 = time.perf_counter()
            filename = 'filename_a_2_0.csv'
            backgroundwrite = AsyncWrite(message,filename)

            backgroundwrite.start()
            backgroundwrite.join()
            # t5 = time.perf_counter()
            new_pressures = [ 0 , 0, 0, i]
            my_client.send_pressures(new_pressures)
        t2 = time.perf_counter()
        my_client.close()
        # t6 = time.perf_counter()
        # print(f'Initialisation of serial Ports Finished in {t2-t1} seconds')
        # print(f'Collection of both sensor and pressures Finished in {t3-t2} seconds')
        # print(f'Collection of only sensor Finished in {t7-t2} seconds')
        # print(f'Collection of only pressures Finished in {t3-t7} seconds')
        # print(f'Creating message string Finished in {t4-t3} seconds')
        # print(f'logging the message string Finished in {t5-t4} seconds')
        # print(f'The whole Main Program Finished in {t6-t1} seconds')
        print(f'The whole filename of { filename} loop 0-2000 by 3 Finished in {t2-t1} seconds')
        
    else:
        print('Connection Issue!')

    print('DONE')
