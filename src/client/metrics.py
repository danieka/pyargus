"""
This file contains all the metrics used by pyargus.

If you want to add a new metric create a new class inheiriting Metric.
This class must implement a static method get_metric() that returns a 
dictionary of metrics in the format {"name": value}.
"""
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
from datetime import timedelta
import sys
import subprocess
import re

class Metric(object):
	pass

class Uptime(Metric):
	@staticmethod
	def get_metric():
		"""This functions returns a metrict for the systems uptime.

		Currently implemented for OSX and Linux."""
		uptime_string = "N/A"
		if sys.platform.startswith("linux2"):
			#This hasn't been tested on a linux machine yet.
			with open('/proc/uptime', 'r') as f:
				uptime_seconds = float(f.readline().split()[0])
		    	uptime_string = str(timedelta(seconds = uptime_seconds))

		if sys.platform.startswith("darwin"):
			p = subprocess.Popen(['uptime'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = p.communicate()
			if err == "":
				l = out.split("  ")[1].split(",")[0:2]
				uptime_string = l[0][3:] + "," + l[1]

		return {"uptime": uptime_string}

class LoadAverages(Metric):
	@staticmethod
	def get_metric():
		load_string = "N/A"
		if sys.platform.startswith("darwin"):
			p = subprocess.Popen(['uptime'], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = p.communicate()
			if err == "":
				load_string = out.split(": ")[1]

		return {"load averages": load_string}

class FreeMemory(Metric):
	@staticmethod
	def get_metric():
		mem_string = "N/A"
		if sys.platform.startswith("darwin"):
			p = subprocess.Popen(["vm_stat"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = p.communicate()
			if err == "":
				line = out.split("\n")[1]
				sep = re.compile(':[\s]+')
				mem_string = str(int(sep.split(line)[1].strip("\."))*4096/1024/1024) + " MB"
				

		return {"free memory": mem_string}

if __name__ == '__main__':
   	pass