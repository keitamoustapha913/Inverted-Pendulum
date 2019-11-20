from opcua import Client
import time
url = "opc.tcp://192.168.142.197:4840"

client = Client(url)

client.connect()
print(" Client Connected ...")

def collecting_pressures():
    global t1
    t1 = time.perf_counter()
    v1 = client.get_node("ns=2;s=|var|CPX-CEC-S1-V3.Application.G.v1")
    S1 = v1.get_value()
    t2 = time.perf_counter()
    print( "S1 = {} of type {} was given at {} seconds".format( S1 , type(S1) , t2-t1 ) )

    t3 = time.perf_counter()
    v2 = client.get_node("ns=2;s=|var|CPX-CEC-S1-V3.Application.G.v2")
    S2 = v2.get_value()
    t4 = time.perf_counter()
    print( "S2 = {} of type {} was given at {} seconds".format( S2 , type(S2) , t4-t3 ) )

    t5 = time.perf_counter()
    v3 = client.get_node("ns=2;s=|var|CPX-CEC-S1-V3.Application.G.v3")
    S3 = v3.get_value()
    t6 = time.perf_counter()
    print( "S3 = {} of type {} was given at {} seconds".format( S3 , type(S3) , t6-t5 ) )

    t7 = time.perf_counter()
    v4 = client.get_node("ns=2;s=|var|CPX-CEC-S1-V3.Application.G.v4")
    S4 = v4.get_value()
    t8 = time.perf_counter()
    print( "S4 = {} of type {} was given at {} seconds".format( S4 , type(S4) , t8-t7 ) )

    t9 = time.perf_counter()
    v4 = client.get_node("ns=2;s=|var|CPX-CEC-S1-V3.Application.PLC_PRG.i" )
    i = v4.get_value()
    t10 = time.perf_counter()
    print( "i = {} of type {} was given at {} seconds".format( i , type(i) , t10-t9 ) )
    
    global t11 
    t11 = time.perf_counter()
    
    print("\n")
    print( " The total time for 5 readings = {} seconds".format( t10-t1 ) )



for loop in range(20):
    collecting_pressures()

    # time.sleep(1)

print( " The disconnect total time for 5 readings = {} seconds".format( t11-t1 ) )

client.disconnect()
