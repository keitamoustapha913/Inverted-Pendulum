# -*- coding: utf-8 -*-

import serial
ser = serial.Serial('COM6',115200,timeout = 0.1)
ser.close()
ser.open()
cmd = [0x02, 0x5A, 0x01, 0xFF, 0x01, 0x01, 0x5C, 0xC7]
ser.write(cmd)
res = ser.read()
print ('réponse :',res)
print ('réponse hex :',res.hex())

sop = [ 0x41]
ser.write(sop)
res = ser.read(3)
print ('réponse new :',res)
print ('réponse new hex :',res.hex())

ser.close()

