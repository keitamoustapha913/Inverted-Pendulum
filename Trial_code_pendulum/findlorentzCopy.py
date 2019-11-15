'''
06 Nov 2019 by Keita Mouhamed Moustapha
'''
import serial.tools.list_ports
import time
from ini_read import getINI

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
            #time.sleep(0.1)
            print('time clock = ', time.clock)
            #print( 'LorenzSerial',[i],' = ',LorenzSerial[i])
            LorenzSerial[i].close()
            #print( 'LorenzSerial',[i], 'closed')
        #print list of Lorenz's serial ports
        #print( 'LorenzSerial = ', LorenzSerial ) 
            
# To send command by Speed Optimized Polling Mode 
def send_polling(LorenzSerial):
    global polling_counter
    polling_counter = polling_counter + 1
    poll_start = [ 0x02, 0x5A, 0x01, 0xFF, 0x01, 0x01, 0x5C, 0xC7 ]
    poll_stop = [ 0x46 ]
    read_a = [ 0x41 ]
    read_b = [ 0x42 ]
    read_ab = [ 0x47 ]

    for i in range(len(LorenzSerial)):
        LorenzSerial[i].open()
        print('Lorenz',[i],' is opened')
        
        LorenzSerial[i].write(poll_start)
        #emptyline = LorenzSerial[i].readline()
        emptyline = LorenzSerial[i].read(2)
        #print('emptyline = ',emptyline)
        
        LorenzSerial[i].write(read_a)
        #line = LorenzSerial[i].readline()
        line = LorenzSerial[i].read(2)
        #print('line = ',line)
        dec_value = int.from_bytes(line,  byteorder = 'big' )
        LorenzSerial[i].close()
        print ('\t dec_value',[i],' = ',dec_value)
        #Sensor_values.append(dec_value)
        Sensor_values[i] = dec_value
        #Sensor_values.insert(i,dec_value)
    print( 'Sensor_values = ', Sensor_values)
    log_data(Sensor_values, polling_counter)
    log_ini()

# to log the sensor values in a row
def log_data(Sensor_values, row_number = 0):
    with open('log.txt',mode = 'a') as log_file:
        data = ( str(row_number)+ ',' + str(Sensor_values[0]) + ',' + str(Sensor_values[1])+ ',' + str(Sensor_values[2])+ ',' + str(Sensor_values[3]) )
        log_file.write(data)
        log_file.write('\n')
        log_file.close()

# To initialize the setup log file
def log_ini():
    with open('init.text', 'w') as dataFile_ini:
        dataFile_ini.write( 'numVariable:2\n' )
        dataFile_ini.write( 'numPoints:2\n' )
        print('I---------------------------------')
        dataFile_ini.write( 'polling_counter:'+ str(polling_counter) )
        dataFile_ini.close()

iniData = getINI()
#numRowsCollect = int(iniData['numRowsCollect'])
#numPoints = int(iniData['numPoints'])


#log_file = open('log.txt',mode = 'w')   
LorenzCOM = []
LorenzSerial = []
Sensor_values = [0,0,0,0]
polling_counter = 0  # counting the number of times the send_polling was called

foundPorts = get_ports()        
connectPort = findLorenz(foundPorts)
print( " Lorenz COM List = ", LorenzCOM)

if connectPort != 'None':
    createLorenzSerials(LorenzCOM)
    #print ( '\n \n','LorenzSerial outside = ', LorenzSerial )
    send_polling(LorenzSerial)
    send_polling(LorenzSerial)
    send_polling(LorenzSerial)
    send_polling(LorenzSerial)
    send_polling(LorenzSerial)
    #print('Before: %s' % time.ctime())
    #time.sleep(1)
    #print('After: %s\n' % time.ctime())
    '''
    ser = serial.Serial(LorenzCOM[0],baudrate = 9600, timeout=1)
    print('Connected to ' + LorenzCOM[0])
    ser.close()
    print('Serial Closed')
    '''

else:
    print('Connection Issue!')

print('DONE')
