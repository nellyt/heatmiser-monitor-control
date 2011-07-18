#
# Neil Trimboy 2011
#
# Despite Heatmiser V3 protocol document stating that current day/h/m/s is on 4 separate addresses [43,46]
# Tests showed that it was not possible to write to individual value anf that all 4 values must be written in a single command
import serial
from struct import pack
import time
import sys
import os

from stats_defn import StatList

# Believe this is known as CCITT (0xFFFF)
# This is the CRC function converted directly from the Heatmiser C code
# provided in their API
class crc16:
    LookupHigh = [
    0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70,
    0x81, 0x91, 0xa1, 0xb1, 0xc1, 0xd1, 0xe1, 0xf1
    ]
    LookupLow = [
    0x00, 0x21, 0x42, 0x63, 0x84, 0xa5, 0xc6, 0xe7,
    0x08, 0x29, 0x4a, 0x6b, 0x8c, 0xad, 0xce, 0xef
    ]
    def __init__(self):
        self.high = 0xff
        self.low = 0xff

    def Update4Bits(self, val):
        # Step one, extract the Most significant 4 bits of the CRC register
        #print "val is %d" % (val)
        t = self.high>>4
        #print "t is %d" % (t)

        # XOR in the Message Data into the extracted bits
        t = t^val
        #print "t is %d" % (t)

        # Shift the CRC Register left 4 bits
        self.high = (self.high << 4)|(self.low>>4)
        self.high = self.high & 0xff    # force char
        self.low = self.low <<4
        self.low = self.low & 0xff  # force char

        # Do the table lookups and XOR the result into the CRC tables
        #print "t for lookup is %d" % (t)
        self.high = self.high ^ self.LookupHigh[t]
        self.high = self.high & 0xff    # force char
        self.low  = self.low  ^ self.LookupLow[t]
        self.low = self.low & 0xff  # force char
        #print "high is %d Low is %d" % (self.high, self.low)

    def CRC16_Update(self, val):
        self.Update4Bits(val>>4) # High nibble first
        self.Update4Bits(val & 0x0f) # Low nibble

    def run(self, message):
        for c in message:
            #print c
            self.CRC16_Update(c)
        #print "CRC is Low %d High  %d" % (self.low, self.high)
        return [self.low, self.high]


# CODE STARTS HERE

DATAOFFSET = 9 # ToDO Move this higher up

# Define magic numbers used in messages
FUNC_READ  = 0
FUNC_WRITE = 1
RW_LENGTH_ALL_HIGH = 0xff
RW_LENGTH_ALL_LOW  = 0xff
CUR_TIME_ADDR = 43
MASTER_ADDR = 0x81

problem = 0

ferr = open('errorlog.txt', 'a')

# Generate a RFC2822 format date
# This works with both Excel and Timeline
localtime = time.asctime( time.localtime(time.time()))
polltime = time.time()
polltimet = time.localtime(polltime)
localtime = time.strftime("%d %b %Y %H:%M:%S +0000", polltimet)
localday = time.strftime("%w", polltimet)

serport = serial.Serial()
serport.port = 6 # 1 less than coim port, USB is 6=com7, ether is 9=10
serport.baudrate = 4800
serport.bytesize = serial.EIGHTBITS
serport.parity = serial.PARITY_NONE
serport.stopbits = serial.STOPBITS_ONE
serport.timeout = 3
try:
    serport.open()
except serial.SerialException, e:
        sys.stderr.write("Could not open serial port %s: %s\n" % (serport.portstr, e))
        s= "%s : Could not open serial port %s: %s\n" % (localtime, serport.portstr, e)
        ferr.write(s)
        problem += 1
        #mail(you, "Heatmiser TimeSet Error ", "Could not open serial port", "errorlog.txt")
        sys.exit(1)

print "COM port configuration is "
print serport.name #Check which port was used
print serport.baudrate
print serport.bytesize
print serport.parity
print serport.stopbits
print serport.timeout
print serport.isOpen()

good = [0,0,0,0,0,0,0,0,0,0,0,0,0] #one bigger than size required YUK
bad =  [0,0,0,0,0,0,0,0,0,0,0,0,0]

badresponse = range(12+1)

# CYCLE THROUGH 12 CONTROLLERS
# This should be a foreach stat
for controller in StatList:
	loop = controller[0]
	print
	print "Testing control %2d in %s *****************************" % (loop, controller[2])
	badresponse[loop] = 0
	# TODO is not V3 controller raise error
	destination = loop
	start_low = (CUR_TIME_ADDR & 0xff)
	start_high = (CUR_TIME_ADDR >> 8) & 0xff
	write_length = 4
	write_length_low = (write_length & 0xff)
	write_length_high = (write_length >> 8) & 0xff
	msgtime = time.time()
	msgtimet = time.localtime(msgtime)
	day  = int(time.strftime("%w", msgtimet))
	if (day == 0):
		day = 7		# Convert python day format to Heatmiser format
	hour = int(time.strftime("%H", msgtimet))
	mins = int(time.strftime("%M", msgtimet))
	secs = int(time.strftime("%S", msgtimet)) % 60 # Need to %60 as pyhton seconds can be  [0,61]
	data = [destination, 10+write_length, MASTER_ADDR, FUNC_WRITE, start_low, start_high, write_length_low, write_length_high, day, hour, mins, secs]
	#print data
	# http://stackoverflow.com/questions/180606/how-do-i-convert-a-list-of-ascii-values-to-a-string-in-python
	#string = ''.join(map(chr,data))
	#print string
	crc = crc16()
	data = data + crc.run(data)
	print data
	string = ''.join(map(chr,data))
	#print string

	#Now try converting it back as a double check
	datal = []
	datal = datal + (map(ord,string))
	#print datal
	msgsenttime = time.strftime("%H:%M:%S", time.localtime(time.time()))
	print msgsenttime
	try:
		written = serport.write(string)  # Write a string
	except serial.SerialTimeoutException, e:
		sys.stderr.write("Write timeout error: %s\n" % (e))
		s= "%s : Write timeout error: %s\n" % (localtime, e)
		ferr.write(s)
		badresponse[loop] += 1

	# Now wait for reply
	byteread = serport.read(100)	# NB max return is 75 in 5/2 mode or 159 in 7day mode
	# @todo must cope with 7 day return size
	#print "Bytes read %d" % (len(byteread) )
	if (len(byteread)) == 7:
		print  "Correct length reply received"
		good[loop] = good[loop] + 1
	else:
		print "Incorrect length reply %s" % (len(byteread))
		bad[loop] = bad[loop] + 1
		s= "%s : Incorrect length reply : %s\n" % (localtime, len(byteread))
		ferr.write(s)
		badresponse[loop] += 1

    # TODO All this should only happen if correct length reply
    #Now try converting it back to array
	datal = []
	datal = datal + (map(ord,byteread))
	# print datal
	# Now check the CRC
	checksum = datal[len(datal)-2:]
	rxmsg = datal[:len(datal)-2]
	# print checksum
	print rxmsg
	crc = crc16() # Initialises the CRC
	expectedchecksum = crc.run(rxmsg)
	if expectedchecksum == checksum:
		print "CRC is correct"
	else:
		print "CRC is INCORRECT"
		s= "%s : Controller %s : Incorrect CRC: %s %s \n" % (localtime, loop, datal, expectedchecksum)
		ferr.write(s)
		badresponse[loop] += 1
		
	# Check the  response
	dest_addr = datal[0]
	frame_len_l = datal[1]
	frame_len_h = datal[2]
	frame_len = (frame_len_h << 8) | frame_len_l
	source_addr = datal[3]
	func_code = datal[4]
	if (dest_addr != MASTER_ADDR):
		print "dest_addr is INCORRECT"
		s= "%s : Controller %s : Incorrect Dest Addr: %s\n" % (localtime, loop, dest_addr)
		ferr.write(s)
		badresponse[loop] += 1
		
	if (frame_len != 7):
		# Reply is always 7 long
		print "response length is INCORRECT"
		s= "%s : Controller %s : Incorrect length: %s\n" % (localtime, loop, frame_len)
		ferr.write(s)
		badresponse[loop] += 1
		
	if (source_addr != loop):
		# Reply is always 7 long
		print "source addr is INCORRECT"
		s= "%s : Controller %s : Incorrect Src Addr: %s\n" % (localtime, loop, source_addr)
		ferr.write(s)
		badresponse[loop] += 1
		
	if (func_code != FUNC_WRITE):
		# Reply is always 7 long
		print "Func Code is INCORRECT"
		s= "%s : Controller %s : Incorrect Func Code: %s\n" % (localtime, loop, func_code)
		ferr.write(s)
		badresponse[loop] += 1

	if badresponse[loop] == 0:
		print "All OK, time set in Controller %s" % loop

	loop = loop+1 # Change to for loop TODO not used
	time.sleep(2) # sleep for 2 seconds before next controller

#END OF CYCLE THROUGH CONTROLLERS

serport.close() # close port
print "Port is now "
print serport.isOpen()
ferr.close()

#if (problem > 0):
	#mail(you, "Heatmiser TimeSet Error ", "A Problem has occurred", "errorlog.txt")

