'''
Using configparser to save an .ini file 
 from https://docs.python.org/3/library/configparser.html


'''

import configparser

#  For writing to a config file

t=1122
config = configparser.ConfigParser()
config['DEFAULT'] = {'ServerAliveInterval': '45',
                      'Compression': 'yes',
                      'CompressionLevel': '9'}
config['bitbucket.org'] = {}
config['bitbucket.org']['User'] = 'hg'
config['topsecret.server.com'] = {}
topsecret = config['topsecret.server.com']
topsecret['Port'] = str(t)     # mutates the parser
topsecret['ForwardX11'] = 'no'  # same here
config['DEFAULT']['ForwardX11'] = 'yes'
with open('example.ini', 'w') as configfile:
    config.write(configfile)


# For reading from a config file

configur = configparser.ConfigParser() 
print (configur.read('example.ini')) 
  
print ("Sections : ", configur.sections()) 
# to return a string
# print ("DEFAULT Library : ", configur.get('DEFAULT','CompressionLevel'))
print( type( configur.get('DEFAULT','CompressionLevel') ) ) 
# print ("Log Errors debugged ? : ", configur.getboolean('debug','log_errors')) 
print ("DEFAULT : ", configur.getint('DEFAULT','ServerAliveInterval'))
# getfloat() raises an exception if the value is not a float
# getint() and getboolean() also do this for their respective types
# a_float = config.getfloat('Section1', 'a_float')
# an_int = config.getint('Section1', 'an_int')
# to return an integer value 
print ("DEFAULT : ", configur.getint('DEFAULT','CompressionLevel'))
# print( type( configur.getint('DEFAULT','CompressionLevel') ) ) 


config['DEFAULT'] = {'ServerAliveInterval': '50',
                      'Compression': 'ysss',
                      'CompressionLevel': '20'}
config['bitbucket.org'] = {}
config['bitbucket.org']['User'] = 'hg'
config['topsecret.server.com'] = {}
topsecret = config['topsecret.server.com']
topsecret['Port'] = str(t + 500)     # mutates the parser
topsecret['ForwardX11'] = 'no'  # same here
config['DEFAULT']['ForwardX11'] = 'yes'
with open('example.ini', 'w') as configfile:
    config.write(configfile)



print (configur.read('example.ini')) 
  
print ("Sections : ", configur.sections()) 
# to return a string
# print ("DEFAULT Library : ", configur.get('DEFAULT','CompressionLevel'))
print( type( configur.get('DEFAULT','CompressionLevel') ) ) 
# print ("Log Errors debugged ? : ", configur.getboolean('debug','log_errors')) 
print ("DEFAULT : ", configur.getint('DEFAULT','ServerAliveInterval'))
# to return an integer value 
print ("DEFAULT : ", configur.getint('DEFAULT','CompressionLevel'))
# print( type( configur.getint('DEFAULT','CompressionLevel') ) ) 

