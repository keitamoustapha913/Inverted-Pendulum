# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:20:36 2019

@author: thomas

Ce programme ouvre le COM7 puis envoie une commande et lit la réponse.
"""



'import win32'
import serial


ser = serial.Serial(timeout = 0.1)
ser.baudrate = 115200
ser.port = 'COM5'
ser.open()
cmd = [0x02, 0x5A, 0x01, 0xFF, 0x01, 0x01, 0x5C, 0xC7]
command  = [0x02, 0x40, 0x01, 0xff, 0x00, 0x40, 0x02,0x02]
command1 = [0x02, 0x5A, 0x01, 0xff, 0x05, 0x03, 0xFA, 0x00, 0x00, 0x41, 0x9D, 0x84]
ser.write(cmd)


line = ser.read(10)
print (type ( line.hex()))
print ('Line :',line.hex())
i = 0;
while (i < 10):
    
    sopm = [ 0x41]
    ser.write(sopm)


    line = ser.read()
    """
    print (type ( line.hex()))
    print ('Line :',line)
    print ('Line :',line.hex(), '\n \n')
    
    num = int.from_bytes(line,  byteorder = 'little' )
    print (type ( num))
    print ('num little :',num)
    """
    numero = int.from_bytes(line,  byteorder = 'big' )
    print ('num big :',numero) # 65109 = 2000mbar we use big endian format
    
    i = i + 1 

ser.close()



ser1 = serial.Serial(timeout = 0.1)
ser1.baudrate = 115200
ser1.port = 'COM6'
ser1.open()
cmd = [0x02, 0x5A, 0x01, 0xFF, 0x01, 0x01, 0x5C, 0xC7]
command  = [0x02, 0x40, 0x01, 0xff, 0x00, 0x40, 0x02,0x02]
command1 = [0x02, 0x5A, 0x01, 0xff, 0x05, 0x03, 0xFA, 0x00, 0x00, 0x41, 0x9D, 0x84]
ser1.write(cmd)


line = ser1.read(10)
print (type ( line.hex()))
print ('Line :',line.hex())
i = 0;
while (i < 10):
    
    sopm = [ 0x41]
    ser1.write(sopm)


    line = ser1.read(1)
    """
    print (type ( line.hex()))
    print ('Line :',line)
    print ('Line :',line.hex(), '\n \n')
    
    num = int.from_bytes(line,  byteorder = 'little' )
    print (type ( num))
    print ('num little :',num)
    """
    numero = int.from_bytes(line,  byteorder = 'big' )
    print ('num big :',numero) # 65109 = 2000mbar we use big endian format
    
    i = i + 1 

ser1.close()







