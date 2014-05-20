import unittest
import socket
import json

from mock import MagicMock
import main



class TestHandleConnection(unittest.TestCase):
	def setUp(self):
		main.clients = []
		self.sock = MagicMock(name='socket', spec=socket.socket)

	def testReportBadData(self):
		self.sock.recv.return_value = "Test"
		main.handle_connection(self.sock)
		self.assertEquals(len(main.clients), 0)

	def testBadCommand(self):
		self.sock.recv.return_value = json.dumps({"command": "bad_command"})
		main.handle_connection(self.sock)
		self.assertEquals(len(main.clients), 0)

	def testRegister(self):
		self.sock.recv.return_value = json.dumps({"command": "register", "hostname": "a"})
		main.handle_connection(self.sock)
		self.assertEquals(len(main.clients), 1)	
		self.assertTrue("a" in main.clients)

	def testReportWithoutRegister(self):
		self.sock.recv.return_value = json.dumps({"command": "report", "hostname": "a"})
		main.handle_connection(self.sock)
		self.assertEquals(len(main.clients), 0)	

	def testRegisterManyHosts(self):
		for i in range(10):
			s = str(i)
			self.sock.recv.return_value = json.dumps({"command": "register", "hostname": s})
			main.handle_connection(self.sock)
		self.assertEquals(len(main.clients), 10)
		for i in range(10):
			s = str(i)
			self.assertTrue(s in main.clients)

	def testRegisterDuplicateHost(self):
		self.sock.recv.return_value = json.dumps({"command": "register", "hostname": "a"})
		main.handle_connection(self.sock)
		self.sock.recv.return_value = json.dumps({"command": "register", "hostname": "a"})
		main.handle_connection(self.sock)
		self.assertEquals(len(main.clients), 1)	
		self.assertTrue("a" in main.clients)


	def testReport(self):
		self.sock.recv.return_value = json.dumps({"command": "register", "hostname": "a"})
		main.handle_connection(self.sock)
		self.sock.recv.return_value = json.dumps({"command": "report", "hostname": "a", "data": "stuff"})
		main.handle_connection(self.sock)
		self.assertEquals(len(main.clients[0].data), 1)
		self.assertEquals(main.clients[0].data["data"], "stuff")	



if __name__ == '__main__':
   	unittest.main()