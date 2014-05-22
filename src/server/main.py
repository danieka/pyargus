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
import socket
import sys
import json
import datetime

clients = []

class Client:
	def __init__(self, data):
		self.hostname = data["hostname"]
		self.last_timestamp = datetime.datetime.now()
		self.data = {}

	def __str__(self):
		s = str(self.hostname) + "\n"
		s += str(self.last_timestamp) + "\n"
		for key, value in self.data.iteritems():
			s += key.capitalize() + ": " + str(value) + "\n"
		return s

	def __eq__(self, other):
		"""This might be what some would call an ugly hack but enables us to compare a hostname-string with this object.
		It is used when we only want to have one instance of every connected host."""
		return self.hostname == other

	def update(self, data):
		self.last_timestamp = datetime.datetime.now()
		data.pop("command")
		data.pop("hostname")
		self.data = data

def handle_connection(c):
	raw_data = c.recv(4096)
	try:
		data = json.loads(raw_data)
	except ValueError, e:
		print e
		print "JSON decoding failed with data:"
		print raw_data
		return
	
	if data["command"] == "register":
		if data["hostname"] not in clients:
			clients.append(Client(data))
	elif data["command"] == "report":
		try:
			clients[clients.index(data["hostname"])].update(data)
		except ValueError, e:
			print e

	c.close()


def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	s.bind((socket.gethostname(), 3314))

	s.listen(5)
	while True:
		try:
			c, addr = s.accept()
			handle_connection(c)

		except KeyboardInterrupt:
			s.close()
			sys.exit()

		for client in clients:
			print client

if __name__ == '__main__':
    main()