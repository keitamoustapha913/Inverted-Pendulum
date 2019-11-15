import OpenOPC
opc = OpenOPC.client()
print (opc.servers() )
opc.connect( 'Matrikon.OPC.Simulation.1')
print ( opc.read(  opc.list('Configured Aliases.init') ) )