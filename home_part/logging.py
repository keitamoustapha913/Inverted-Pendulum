from random import randint
import time


sensor_readings = []
pressure_readings = [ ]

def collect_sensors():
    '''
    To simulate the sensor readings collected with random integer values 
    
    Return list of 4 sensor random values
    '''
    for i in range(4):
        sensor_readings.append(randint(0,10000))

    return sensor_readings

def collect_pressures():
    for i in range(4):
        pressure_readings.append(randint(0,2000))

    return pressure_readings






if __name__ == "__main__":
    print("Hello World ")

    sensor_readings = collect_sensors()
    print( f'Sensor Readings = {sensor_readings}' )

    pressure_readings = collect_pressures()
    print( f'pressure_readings = {pressure_readings}' )



