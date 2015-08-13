import xmlrpclib, httplib

# class ProxiedTransport(xmlrpclib.Transport):
    # def set_proxy(self, proxy):
        # self.proxy = proxy
    # def make_connection(self, host):
        # self.realhost = host
        # h = httplib.HTTP(self.proxy)
        # return h
    # def send_request(self, connection, handler, request_body):
        # connection.putrequest("POST", 'http://%s%s' % (self.realhost, handler))
    # def send_host(self, connection, host):
        # connection.putheader('Host', self.realhost)

# p = ProxiedTransport()
# p.set_proxy('http://betty.userland.com')
# server = xmlrpclib.Server('http://time.xmlrpc.com/RPC2', transport=p)
# print server.currentTime.getCurrentTime()


# simple test program (from the XML-RPC specification)
from xmlrpclib import ServerProxy, Error

# server = ServerProxy("http://localhost:8000") # local server
server = ServerProxy("http://betty.userland.com")

print server

try:
    print server.examples.getStateName(41)
except Error as v:
    print "ERROR", v
	
try:
    print server.examples.getCurrentTime()
except Error as v:
    print "ERROR", v
	
