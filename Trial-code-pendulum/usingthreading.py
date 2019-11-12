'''
12 Nov 2019 by Keita Mouhamed Moustapha

using threading and time modules
'''
import serial.tools.list_ports
import time
import concurrent.futures

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
            #LorenzSerial[i] = serial.Serial(port=LorenzCOM[i], baudrate=115200, timeout= 0.1)
            LorenzSerial.append( serial.Serial(port=LorenzCOM[i], baudrate=115200, timeout= 0.1) )
            #print( 'LorenzSerial',[i],' = ',LorenzSerial[i])
            LorenzSerial[i].close()
            #print( 'LorenzSerial',[i], 'closed')
        #print list of Lorenz's serial ports
        #print( 'LorenzSerial = ', LorenzSerial ) 
            
# To send command by Speed Optimized Polling Mode with threading
def Thread_send_polling(LorenzSerial):
    poll_start = [ 0x02, 0x5A, 0x01, 0xFF, 0x01, 0x01, 0x5C, 0xC7 ]
    poll_stop = [ 0x46 ]
    read_a = [ 0x41 ]
    read_b = [ 0x42 ]
    read_ab = [ 0x47 ]

    LorenzSerial.open()
    # print('Lorenz',LorenzSerial,' is opened')
    LorenzSerial.write(poll_start)
    emptyline = LorenzSerial.read(2)
    LorenzSerial.write(read_a)
    line = LorenzSerial.read(2)
    numero = int.from_bytes(line,  byteorder = 'big' )
    LorenzSerial.close()
    print ('\t numero  = ',numero)


# To send command by Speed Optimized Polling Mode without threading
def send_polling(LorenzSerial):
    poll_start = [ 0x02, 0x5A, 0x01, 0xFF, 0x01, 0x01, 0x5C, 0xC7 ]
    poll_stop = [ 0x46 ]
    read_a = [ 0x41 ]
    read_b = [ 0x42 ]
    read_ab = [ 0x47 ]

    t1 = time.perf_counter()
    for i in range(len(LorenzSerial)):
        LorenzSerial[i].open()
        # print('Lorenz',[i],' is opened')
        LorenzSerial[i].write(poll_start)
        emptyline = LorenzSerial[i].read(2)
        LorenzSerial[i].write(read_a)
        line = LorenzSerial[i].read(2)
        numero = int.from_bytes(line,  byteorder = 'big' )
        LorenzSerial[i].close()
        print ('\t numero',[i],' = ',numero)
    t2 = time.perf_counter()
    print(f'Without Threading Finished in {t2-t1} seconds')

        
LorenzCOM = []
LorenzSerial = []


if __name__ == "__main__":

    foundPorts = get_ports()        
    connectPort = findLorenz(foundPorts)
    print( " Lorenz COM List = ", LorenzCOM)

    if connectPort != 'None':
        createLorenzSerials(LorenzCOM)
        #print ( '\n \n','LorenzSerial outside = ', LorenzSerial )
        send_polling(LorenzSerial)
        t1 = time.perf_counter()

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(Thread_send_polling, LorenzSerial)

        t2 = time.perf_counter()
        print(f'with Process Finished in {t2-t1} seconds')

        t1 = time.perf_counter()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(Thread_send_polling, LorenzSerial)

        t2 = time.perf_counter()
        print(f'with Thread Finished in {t2-t1} seconds')

        '''
        ser = serial.Serial(LorenzCOM[0],baudrate = 9600, timeout=1)
        print('Connected to ' + LorenzCOM[0])
        ser.close()
        print('Serial Closed')
        '''

    else:
        print('Connection Issue!')

    print('DONE')
