"""The MIT License (MIT)

Copyright (c) 2014 Daniel Karlsson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
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

class TestClient(unittest.TestCase):

	def setUp(self):
		self.c = main.Client({"hostname": "a"})

	def testBadInitData(self):
		c = main.Client({"hostname": 1})
		print c


if __name__ == '__main__':
   	unittest.main()