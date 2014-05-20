import socket
import json
import time
import metrics
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.connect((socket.gethostname(), 3314))
data = {"command": "register", "hostname": socket.gethostname()}
s.send(json.dumps(data))
s.close()

while True:
	data = {"command": "report", "hostname": socket.gethostname()}
	for function in metrics.metrics:
		result = function()
		data.update(result)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	s.connect((socket.gethostname(), 3314))
	s.send(json.dumps(data))
	s.close()
	sys.exit()

