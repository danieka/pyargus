from datetime import timedelta
import sys
import subprocess



def uptime():
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

	return ["uptime", uptime_string]

def load_averages():

	load_string = "N/A"
	if sys.platform.startswith("darwin"):
		p = subprocess.Popen(['uptime'], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
		out, err = p.communicate()
		if err == "":
			load_string = out.split(": ")[1]

	return ["load averages", load_string]

metrics = [uptime, load_averages]