from random import randint
import time
from fileclass import AsyncWrite

sensor_readings = []
pressure_readings = [ ]
message_log = ''

def collect_sensors():
    '''
    To simulate the sensor readings collected with random integer values 
    
    Return list of 4 sensor random values
    '''
    for _ in range(4):
        sensor_readings.append(randint(0,10000))

    return sensor_readings

def collect_pressures():
    for _ in range(4):
        pressure_readings.append(randint(0,2000))

    return pressure_readings






if __name__ == "__main__":

    print("Hello World ")
    t1 = time.perf_counter()

    sensor_readings = collect_sensors()
    # print( f'Sensor Readings = {sensor_readings}' )

    pressure_readings = collect_pressures()
    # print( f'pressure_readings = {pressure_readings}' )

    for reading in sensor_readings:
        message_log += str(reading) + ','

    for reading in pressure_readings:
        if pressure_readings.index(reading) < ( len(pressure_readings) -1 ):
            message_log += str(reading) + ','
        else:
            message_log += str(reading)

    # print(message_log)
    
    backgroundfile_log = AsyncWrite(message_log,'home_file.txt')

    backgroundfile_log.start()
    backgroundfile_log.join()

    t2 = time.perf_counter()
    
    print(f'Background file finished in {t2-t1} seconds ')
    








