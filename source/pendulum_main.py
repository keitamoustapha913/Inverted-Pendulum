'''
15 Nov 2019 by Keita Mouhamed Moustapha

'''
import serial.tools.list_ports
import time
import concurrent.futures
import os
import multiprocessing
import sys
import threading



def get_ports():
    ports = serial.tools.list_ports.comports()
    return ports

def findLorenz(portsFound):
    commPort = 'None'
    numConnection = len(portsFound)
    
    for i in range(0,numConnection):
        port = foundPorts[i]
        strPort = str(port)
        if 'Lorenz' in strPort:
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])
            LorenzCOM.append(commPort)
    return commPort

# To create list of 4 Lorenz Serial objects
def createLorenzSerials(LorenzCOM):
    if len(LorenzCOM) == 4:
        #print('All LorenzCOM connections detected ' )
        for i in range(len(LorenzCOM)):
            LorenzSerials.append( serial.Serial(port=LorenzCOM[i], baudrate=115200, timeout= 0.1) )
            LorenzSerials[i].close()




