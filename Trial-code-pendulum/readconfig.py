from configparser import ConfigParser 
  
configur = ConfigParser() 
print (configur.read('example.ini')) 
  
print ("Sections : ", configur.sections()) 
print ("Installation Library : ", configur.get('installation','library')) 
print ("Log Errors debugged ? : ", configur.getboolean('debug','log_errors')) 
print ("Port Server : ", configur.getint('server','port')) 
print ("Worker Server : ", configur.getint('server','nworkers'))