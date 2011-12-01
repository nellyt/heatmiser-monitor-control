#
# Neil Trimboy 2011
#
# Sets current time/date to all controllers
#
# Despite Heatmiser V3 protocol document stating that current day/h/m/s is on 4 separate addresses [43,46]
# Tests showed that it was not possible to write to individual value anf that all 4 values must be written in a single command
import serial
from struct import pack
import time
import sys
import os

#from stats_defn import StatList
from stats_defn import *
from hm_constants import *
from hm_utils import *

# CODE STARTS HERE

# Define magic numbers used in messages
MASTER_ADDR = 0x81

problem = 0

#ferr = open('errorlog2.txt', 'a')
sys.stderr = open('errorlog.txt', 'a') # Redirect stderr

# Generate a RFC2822 format date
# This works with both Excel and Timeline
localtime = time.asctime( time.localtime(time.time()))
polltime  = time.time()
polltimet = time.localtime(polltime)
localtime = time.strftime("%d %b %Y %H:%M:%S +0000", polltimet)
localday  = time.strftime("%w", polltimet)

serport = serial.Serial()
serport.port     = 6 # 1 less than coim port, USB is 6=com7, ether is 9=10
serport.baudrate = 4800
serport.bytesize = serial.EIGHTBITS
serport.parity   = serial.PARITY_NONE
serport.stopbits = serial.STOPBITS_ONE
serport.timeout  = 3
try:
    serport.open()
except serial.SerialException, e:
        s= "%s : Could not open serial port %s: %s\n" % (localtime, serport.portstr, e)
        sys.stderr.write(s)
        problem += 1
        #mail(you, "Heatmiser TimeSet Error ", "Could not open serial port", "errorlog.txt")
        sys.exit(1)

print "%s port configuration is %s" % (serport.name, serport.isOpen())
print "%s baud, %s bit, %s parity, with %s stopbits, timeout %s seconds" % (serport.baudrate, serport.bytesize, serport.parity, serport.stopbits, serport.timeout)

#good = [0,0,0,0,0,0,0,0,0,0,0,0,0] # TODO one bigger than size required YUK
#bad =  [0,0,0,0,0,0,0,0,0,0,0,0,0]

badresponse = range(12+1) #TODO hardcoded 12 here! YUK

# CYCLE THROUGH ALL CONTROLLERS
for controller in StatList:
	loop = controller[0]
	print
	print "Testing control %2d in %s *****************************" % (loop, controller[2])
	badresponse[loop] = 0
	# TODO is not V3 controller raise error
	destination = loop
	msgtime = time.time()
	msgtimet = time.localtime(msgtime)
	day  = int(time.strftime("%w", msgtimet))
	if (day == 0):
		day = 7		# Convert python day format to Heatmiser format
	hour = int(time.strftime("%H", msgtimet))
	mins = int(time.strftime("%M", msgtimet))
	secs = int(time.strftime("%S", msgtimet))
	if (secs == 61):
		secs = 60 # Need to do this as pyhton seconds can be  [0,61]
	print "%d %d:%d:%d" % (day, hour, mins, secs)
	payload = [day, hour, mins, secs]
	msg = hmFormMsgCRC(destination, controller[SL_CONTR_TYPE], MASTER_ADDR, FUNC_WRITE, CUR_TIME_ADDR, payload)
	print msg
	# http://stackoverflow.com/questions/180606/how-do-i-convert-a-list-of-ascii-values-to-a-string-in-python
	string = ''.join(map(chr,msg))
	#print string

	#Now try converting it back as a double check
	#datal = []
	#datal = datal + (map(ord,string))
	#print datal
	try:
		written = serport.write(string)  # Write a string
	except serial.SerialTimeoutException, e:
		s= "%s : Write timeout error: %s\n" % (localtime, e)
		sys.stderr.write(s)
		badresponse[loop] += 1

	# Now wait for reply
	byteread = serport.read(100)	# NB max return is 75 in 5/2 mode or 159 in 7day mode
	# @todo must cope with 7 day return size

	#Now try converting it back to array
	datal = []
	datal = datal + (map(ord,byteread))
	
	if (hmVerifyMsgCRCOK(MASTER_ADDR, controller[3], destination, FUNC_WRITE, 2, datal) == False):
		badresponse[loop] += 1

	if badresponse[loop] == 0:
		print "All OK, time set in Controller %s" % loop

	loop = loop+1 # Change to for loop TODO not used
	time.sleep(2) # sleep for 2 seconds before next controller

#END OF CYCLE THROUGH CONTROLLERS

serport.close() # close port
print "Port is now %s" % serport.isOpen()
#ferr.close()

#if (problem > 0):
	#mail(you, "Heatmiser TimeSet Error ", "A Problem has occurred", "errorlog.txt")
