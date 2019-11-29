'''
This is file class to write and read files 

Reference : https://www.tutorialspoint.com/writing-files-in-background-in-python
Started 15 Nov 2019 by keita Mouhamed Moustapha

'''

import threading
import time
import csv

class AsyncWrite(threading.Thread):
      '''
      Class instance declaration for background writing

      '''
      def __init__(self, text, filename):             
         '''
         Initialise data to file in the background 
         :param text: (string) text message to be written
         :param filename: (string) filename with ext like .csv , .txt
         :return: None

         '''
         threading.Thread.__init__(self)
         self.text = text
         self.filename = filename
      def run(self):
         """
         To Write the text to filename.ext in the background
         """
         with open(self.filename, 'a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(self.text)


def Main():
   """
   A sample code to show the use of AsyncWrite class
   """
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