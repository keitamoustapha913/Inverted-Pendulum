from opcua import Client
import time

'''
url = "opc.tcp://192.168.142.197:4840"

opc_client = Client(url)

opc_client.connect()
print(" opc_client Connected ...")
'''

class Opc_Client():
    def __init__(self, end_point_url = "opc.tcp://192.168.142.197:4840" ):
        self.end_point_url = end_point_url
        self.opc_client = Client( end_point_url )
        self.pressure_node_1 = None
        self.pressure_node_2 = None
        self.pressure_node_3 = None
        self.pressure_node_4 = None
        self.pressure_node_list = []
        self.connect()


    def connect(self):
        '''
        To connect to the server defined at end_point_url
        '''
        self.opc_client.connect()
        print(" opc_client is successfully connected at {} ...".format( self.end_point_url ) )
        list = self.get_pressure_nodes()
        print(" List of nodes connected to ... \n \n{} \n{} \n{} \n{}\n".format( list[0] , list[1] , list[2] , list[3] ) )

    def get_pressure_nodes(self):
        self.pressure_node_1 = self.opc_client.get_node("ns=2;s=|var|CPX-CEC-S1-V3.Application.G.v1")
        self.pressure_node_2 = self.opc_client.get_node("ns=2;s=|var|CPX-CEC-S1-V3.Application.G.v2")
        self.pressure_node_3 = self.opc_client.get_node("ns=2;s=|var|CPX-CEC-S1-V3.Application.G.v3")
        self.pressure_node_4 = self.opc_client.get_node("ns=2;s=|var|CPX-CEC-S1-V3.Application.G.v4")
        self.pressure_node_list = [ self.pressure_node_1 , self.pressure_node_2 , self.pressure_node_3 , self.pressure_node_4]
        return self.pressure_node_list

    def collecting_pressures(self):
        '''
        To collect all the four pressures that is output of the FESTO valves in mbar

        Return list of four pressures
        '''
        t1 = time.perf_counter()
        pressure_reading1 = self.pressure_node_1.get_value()
        t2 = time.perf_counter()
        print( "pressure_reading 1 = {} of type {} was given at {} seconds".format( pressure_reading1 , type(pressure_reading1) , t2-t1 ) )

        t3 = time.perf_counter()
        pressure_reading2 = self.pressure_node_2.get_value()
        t4 = time.perf_counter()
        print( "pressure_reading 2 = {} of type {} was given at {} seconds".format( pressure_reading2 , type(pressure_reading2) , t4-t3 ) )

        t5 = time.perf_counter()
        pressure_reading3 = self.pressure_node_3.get_value()
        t6 = time.perf_counter()
        print( "pressure_reading 3 = {} of type {} was given at {} seconds".format( pressure_reading3 , type(pressure_reading3) , t6-t5 ) )

        t7 = time.perf_counter()
        pressure_reading4 = self.pressure_node_4.get_value()
        t8 = time.perf_counter()
        print( "pressure_reading 4 = {} of type {} was given at {} seconds".format( pressure_reading4 , type(pressure_reading4) , t8-t7 ) )
        t10 = time.perf_counter()
        
        print("\n")
        print( " The total time for 5 readings = {} seconds".format( t10-t1 ) )

        return [ pressure_reading1 , pressure_reading2 , pressure_reading3 , pressure_reading4  ]

    def send_pressures(self, pressure_values = [0 , 0 , 0 , 0 ] ):
        if len(pressure_values) == 4:
            for node, pressure_value in zip(self.pressure_node_list, pressure_values):
                node.set_value(pressure_value)

    def close(self):
        self.opc_client.disconnect()
        print( " Successfully disconnected....." )


if __name__ == "__main__":
    my_client = Opc_Client()

    for i in range(10):
        my_pressures_readings = my_client.collecting_pressures()

    my_client.close()
