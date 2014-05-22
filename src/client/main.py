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
import json
import time
import metrics
import sys
from ConfigParser import SafeConfigParser

def main():
	parser = SafeConfigParser()
	parser.read('client/config.ini')

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	s.connect((parser.get("network", "server"), 3314))
	data = {"command": "register", "hostname": socket.gethostname()}
	s.send(json.dumps(data))
	s.close()

	while True:
		data = {"command": "report", "hostname": socket.gethostname()}
		for metric_class in metrics.Metric.__subclasses__():
			result = metric_class.get_metric()
			data.update(result)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		s.connect((socket.gethostname(), 3314))
		s.send(json.dumps(data))
		s.close()
		time.sleep(int(parser.get("general", "update_interval")))

if __name__ == '__main__':
    main()