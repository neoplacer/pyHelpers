import xmlrpclib

server_url = 'https://evatr.bff-online.de/'
server     = xmlrpclib.Server(server_url)

# daten zum testen
UstId_1    = 'DEXXXXXXXXXXXXXX'
UstId_2    = 'ITXXXXXXXXXXXXXX'
Firmenname = 'Firmenname einschl. Rechtsform'
Ort        = 'Ort'
PLZ        = '1234567'
Strasse    = 'Strasse und Hausnummer'
Druck      = 'nein'

rpc = server.evatrRPC(UstId_1, UstId_2, Firmenname, Ort, PLZ, Strasse, Druck)

print rpc