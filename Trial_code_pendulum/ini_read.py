#dataFile_ini = open('dataSetup.ini', 'r')
ini_data_result = {}

def getINI():
    with open('init.txt', 'r') as dataFile_ini:
        iniHeader = dataFile_ini.readline().split(':')
        print( 'iniHeader = ', iniHeader )
        print(iniHeader[0] + ' ' + iniHeader[1].rstrip() )
        iniReadLines = int(iniHeader[1].rstrip())
        print( 'iniReadLines = ', iniReadLines)

        for i in range(0,iniReadLines):
            
            variable = dataFile_ini.readline().split(':')
            print( 'variable = ' , variable)
            ini_data_result[variable[0]] = variable[1].rstrip()
            
        print( 'ini_data_result = ',ini_data_result)
        
    return ini_data_result
