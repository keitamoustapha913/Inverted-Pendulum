'''
https://www.tutorialspoint.com/writing-files-in-background-in-python
15 Nov 2019

'''

import threading
import time


class AsyncWrite(threading.Thread):
      '''
      To write data to file in the background
      '''
      def __init__(self, text, filename):
         threading.Thread.__init__(self)
         self.text = text
         self.filename = filename
      def run(self):
         f = open(self.filename, "a")
         f.write(self.text + '\n')
         f.close()
         time.sleep(1)
         print ("Finished Background file write to " + self.filename)

def Main():
   message = input("Enter a string to store:" )
   background = AsyncWrite(message,'filename.txt')
   #print threading.enumerate()
   background.start()
   print ("The program can continue while it writes in another thread")
   num = int(input("Entered number is : "))
   if (num%2==0):
      print("Entered number is Even")
   else:
      print("Entered number is ODD")
   background.join()
   print ("Waited until thread was complete")
   # print (threading.enumerate())

if __name__ == '__main__':
   Main()