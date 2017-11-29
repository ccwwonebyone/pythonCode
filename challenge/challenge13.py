from xmlrpc import client
server = client.Server('http://www.pythonchallenge.com/pc/phonebook.php')
#print server.system.listMethods()
print(server.phone('Bert'))