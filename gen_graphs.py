#
# Neil Trimboy 2011
#

from struct import pack
import time
import sys

import os

from stats_defn import StatList

d = os.path.join(os.getcwd(),"graphs")
if not os.path.exists(d):
	os.makedirs(d)
	
problem = 0

rrdfile = 'hmstats.rrd'
rrdrocfile = 'hmoptimstart.rrd'
rrdtimeerrfile = 'hmtimedelta.rrd'

graphs = [
#["Today"],
#["Yesterday"],
#["ThisWeek"],
#["LastWeek"],
#["ThisMonth"],
#["LastMonth"],
["24Hrs", '-24hour', 'now'],
["7days", '-7day', 'now'],
["4Weeks", '-4week', 'now'],
["8Weeks", '-8week', 'now'],
["12Weeks", '-12week', 'now'],
]

for graph in graphs:
	for controller in StatList:
		start_time = graph[1]  
		output_filename = 'graphs/' + controller[1] + '_' + graph[0] + '.png'
		end_time = graph[2]
		ds_name = 'Air'
		ds_name2 = 'Floor'
		ds_name3 = 'Set'
		ds_name4 = 'Demand'
		width = '400'
		height = '150'
		cur_date = time.strftime('%m/%d/%Y %H\:%M\:%S', time.localtime())       
		cmd_graph = 'rrdtool graph ' + output_filename + \
			' DEF:' + ds_name + '=' + rrdfile + ':' + controller[1] + 'air' + ':AVERAGE' + \
			' DEF:' + ds_name2 + '=' + rrdfile + ':' + controller[1] + 'flr' + ':AVERAGE' + \
			' DEF:' + ds_name3 + '=' + rrdfile + ':' + controller[1] + 'set' + ':AVERAGE' + \
			' DEF:' + ds_name4 + '=' + rrdfile + ':' + controller[1] + 'dem' + ':MAX' + \
			' VDEF:' + ds_name  + 'last=' + ds_name  + ',LAST' + \
			' VDEF:' + ds_name2 + 'last=' + ds_name2 + ',LAST' + \
			' VDEF:' + ds_name3 + 'last=' + ds_name3 + ',LAST' + \
			' COMMENT:"Generated ' + cur_date + '\\n"' + \
			' AREA:' + ds_name + '#FFFF00' + ':"Air"'\
			' GPRINT:' + ds_name  + 'last:"Current Air   = %6.2lf%S"' + \
			' LINE:' + ds_name2 + '#FF0000' + ':"Floor"'\
			' GPRINT:' + ds_name2 + 'last:"Current Floor = %6.2lf%S"' + \
			' LINE:' + ds_name3 + '#008000' + ':"Set"'\
			' GPRINT:' + ds_name3 + 'last:"Current Set   = %6.2lf%S"' + \
			' LINE:' + ds_name4 + '#000000' + \
			' --title="Room ' + controller[2] + ' ' + graph[0] + '"' + \
			' --vertical-label="Celcius"' + \
			' --start=' + start_time + \
			' --end=' + end_time + \
			' --width=1000' + \
			' --height=300'
					# ' GPRINT:' + ds_name  + 'last:"                         Current Air   = %6.2lf%S"' + \
			# ' GPRINT:' + ds_name2 + 'last:"                         Current Floor = %6.2lf%S"' + \
			# ' GPRINT:' + ds_name3 + 'last:"                         Current Set   = %6.2lf%S"' + \
		#	' VDEF:' + ds_name + 'last=' + ds_name + ',LAST' + \
		#	' VDEF:' + ds_name + 'avg=' + ds_name + ',AVERAGE' + \
		#	' COMMENT:"' + cur_date + '"' + \
		#	' GPRINT:' + ds_name + 'avg:"                         average=%6.2lf%S"' + \
		# ' --title=Room "' + rrdfile +'"' + \
		# ' --lower-limit="0"'
		print cmd_graph
		cmd = os.popen4(cmd_graph)
		cmd_output = cmd[1].read()
		for fd in cmd: fd.close()
		if len(cmd_output) > 0:
			print cmd_output
			
# Now the optimstart graph
start_time = '-8week'  
output_filename = 'graphs/' + 'optimstart.png'
end_time = 'now'
width = '400'
height = '150'
cur_date = time.strftime('%m/%d/%Y %H\:%M\:%S', time.localtime())       
cmd_graph = 'rrdtool graph ' + output_filename
for controller in StatList:
	cmd_graph += ' DEF:' + controller[1] + 'roc=' + rrdrocfile + ':' + controller[1] + 'roc' + ':AVERAGE'
	cmd_graph += ' DEF:' + controller[1] + 'os=' + rrdrocfile + ':' + controller[1] + 'optimstart' + ':AVERAGE'
	cmd_graph += ' LINE:' + controller[1] + 'roc#' + controller[4] + ':' + controller[1]
	cmd_graph += ' LINE:' + controller[1] + 'os#' + controller[4]
	cmd_graph += ' VDEF:' + controller[1]  + 'last=' + controller[1] + 'roc' + ',LAST'
	cmd_graph += ' GPRINT:' + controller[1]  + 'last:"' + controller[1] + ' ROC   = %6.2lf%S"'
			  
cmd_graph += ' COMMENT:"Generated ' + cur_date + '"' + \
' --title="Optim Start Data"' + \
' --vertical-label="mins per degree"' + \
' --start=' + start_time + \
' --end=' + end_time + \
' --width=1000' + \
' --height=300'
print cmd_graph
cmd = os.popen4(cmd_graph)
cmd_output = cmd[1].read()
for fd in cmd: fd.close()
if len(cmd_output) > 0:
	print cmd_output

# Now the timeerr graph
start_time = '-14day'  
output_filename = 'graphs/' + 'timeerr.png'
end_time = 'now'
width = '400'
height = '150'
cur_date = time.strftime('%m/%d/%Y %H\:%M\:%S', time.localtime())       
cmd_graph = 'rrdtool graph ' + output_filename
for controller in StatList:
	cmd_graph += ' DEF:' + controller[1] + 'err=' + rrdtimeerrfile + ':' + controller[1] + 'timedelta' + ':AVERAGE'
	cmd_graph += ' LINE:' + controller[1] + 'err#' + controller[4] + ':' + controller[1]
	cmd_graph += ' VDEF:' + controller[1]  + 'last=' + controller[1] + 'err' + ',LAST'
	cmd_graph += ' GPRINT:' + controller[1]  + 'last:"' + controller[1] + ' Err   = %6.1lf%S"'
			
cmd_graph += ' COMMENT:"Generated ' + cur_date + '"' + \
' --title="Time Error Data"' + \
' --vertical-label="seconds"' + \
' --start=' + start_time + \
' --end=' + end_time + \
' --width=1000' + \
' --height=300' + \
' --upper-limit=300' + \
' --lower-limit=-300' + \
' --rigid'
print cmd_graph
cmd = os.popen4(cmd_graph)
cmd_output = cmd[1].read()
for fd in cmd: fd.close()
if len(cmd_output) > 0:
	print cmd_output
	
#From heating.py
# Last four weeks: --start end-4w --end 00:00
# January 2001:    --start 20010101 --end start+31d
# January 2001:    --start 20010101 --end 20010201
# Last hour:       --start end-1h
# Last 24 hours:   <nothing at all>
# Yesterday:       --end 00:00

# last 24ht
# last 7d
# yesterday
# previous week
# period file title
# start end filename Title
#-1day +24h 24hrs "Previous 24hrs"

# @todo move to gengraphs.py
for controller in StatList:
	start_time = '-3day'  
	output_filename = 'graphs/' + controller[1] + '.png'
	end_time = 'now'
	ds_name = 'Air'
	ds_name2 = 'Floor'
	ds_name3 = 'Set'
	ds_name4 = 'Demand'
	width = '400'
	height = '150'
	cur_date = time.strftime('%m/%d/%Y %H\:%M\:%S', time.localtime())       
	cmd_graph = 'rrdtool graph ' + output_filename + \
		' DEF:' + ds_name + '=' + rrdfile + ':' + controller[1] + 'air' + ':AVERAGE' + \
		' DEF:' + ds_name2 + '=' + rrdfile + ':' + controller[1] + 'flr' + ':AVERAGE' + \
		' DEF:' + ds_name3 + '=' + rrdfile + ':' + controller[1] + 'set' + ':AVERAGE' + \
		' DEF:' + ds_name4 + '=' + rrdfile + ':' + controller[1] + 'dem' + ':MAX' + \
		' VDEF:' + ds_name  + 'last=' + ds_name  + ',LAST' + \
		' VDEF:' + ds_name2 + 'last=' + ds_name2 + ',LAST' + \
		' VDEF:' + ds_name3 + 'last=' + ds_name3 + ',LAST' + \
		' COMMENT:"' + cur_date + '\\n"' + \
		' AREA:' + ds_name + '#FFFF00' + ':"Air"'\
		' GPRINT:' + ds_name  + 'last:"Current Air   = %6.2lf%S"' + \
		' LINE:' + ds_name2 + '#FF0000' + ':"Floor"'\
		' GPRINT:' + ds_name2 + 'last:"Current Floor = %6.2lf%S"' + \
		' LINE:' + ds_name3 + '#008000' + ':"Set"'\
		' GPRINT:' + ds_name3 + 'last:"Current Set   = %6.2lf%S"' + \
		' LINE:' + ds_name4 + '#000000' + \
		' --title="Room ' + controller[2] +'"' + \
		' --vertical-label="Celcius"' + \
		' --start=' + start_time + \
		' --end=' + end_time + \
		' --width=1000' + \
		' --height=300'
				# ' GPRINT:' + ds_name  + 'last:"                         Current Air   = %6.2lf%S"' + \
		# ' GPRINT:' + ds_name2 + 'last:"                         Current Floor = %6.2lf%S"' + \
		# ' GPRINT:' + ds_name3 + 'last:"                         Current Set   = %6.2lf%S"' + \
	#	' VDEF:' + ds_name + 'last=' + ds_name + ',LAST' + \
	#	' VDEF:' + ds_name + 'avg=' + ds_name + ',AVERAGE' + \
	#	' COMMENT:"' + cur_date + '"' + \
	#	' GPRINT:' + ds_name + 'avg:"                         average=%6.2lf%S"' + \
	# ' --title=Room "' + rrdfile +'"' + \
	# ' --lower-limit="0"'
	#
	# next lines now commented out 
	# @todo move to gengraphs.py
	#print cmd_graph
	#cmd = os.popen4(cmd_graph)
	#cmd_output = cmd[1].read()
	#for fd in cmd: fd.close()
	#if len(cmd_output) > 0:
	#	print cmd_output
