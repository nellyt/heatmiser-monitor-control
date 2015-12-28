# Introduction #

Some python scripts to interact with Heatmiser thermostats.
http://www.heatmiser.co.uk

## Aims/Motivations ##
  * To read data from a set of controllers and present this info to see what my heating system was up to
  * Gather some historical data

## Current Features ##
  * Web page of current heating status of all controllers
  * Web page of currently programmed times of all controllers
  * Web page of current settings/status of all parameters in all controllers
  * RRD records of all controllers of temeratures
  * Utility to set time in all controllers
  * Graphical timeline of heating status
  * Emailed alarms for error conditions

## Screenshots ##
![http://heatmiser-monitor-control.googlecode.com/svn/wiki/heating_status.png](http://heatmiser-monitor-control.googlecode.com/svn/wiki/heating_status.png)
![http://heatmiser-monitor-control.googlecode.com/svn/wiki/heating_config.png](http://heatmiser-monitor-control.googlecode.com/svn/wiki/heating_config.png)
![http://heatmiser-monitor-control.googlecode.com/svn/wiki/heating_times.png](http://heatmiser-monitor-control.googlecode.com/svn/wiki/heating_times.png)
![http://heatmiser-monitor-control.googlecode.com/svn/wiki/heattime.png](http://heatmiser-monitor-control.googlecode.com/svn/wiki/heattime.png)
![http://heatmiser-monitor-control.googlecode.com/svn/wiki/heating_times.png](http://heatmiser-monitor-control.googlecode.com/svn/wiki/heating_times.png)
![http://heatmiser-monitor-control.googlecode.com/svn/wiki/Study_7days.png](http://heatmiser-monitor-control.googlecode.com/svn/wiki/Study_7days.png)

# Requirements #
I am using Python 2.7
You also need PySerial http://pyserial.sourceforge.net/

# Details #

Add your content here.  Format your content with:
  * Text in **bold** or _italic_
  * Headings, paragraphs, and lists
  * Automatic links to other wiki pages


There seem to be two generations of controllers in the field using what is known as V2 and V3 protocols.
V2 is simpler and has been reverse engineered.
V3 is publicly available at http://www.heatmiser.co.uk/support/admin/attachments/protocolv3system.pdf

This code currently supports only V3

# Other projects/info online #

## Limitations ##
  * Currently supports only V3, extension would be quite easy [issue #1](https://code.google.com/p/heatmiser-monitor-control/issues/detail?id=#1)
  * Display currently only compatible with 5/2 mode

# Hardware #
Controllers use RS485.
I am connected using a USB to RS485 adapter

# Coding #
This was a learning exercise in python for me and so a lot of code was experimental.
Functionality is more important than elegance to me at this point, given time I hope to tidy things.
Some of the code is dire but has been posted here before I'd really like as it has been requested. I hope to tidy it up in the coming weeks.
It has been running reliably for me for several months.

# Where is this going #
Client side display/processing of the data provided the quickest way to getting the functionality I wanted with a rapidly approaching winter.
This is not ideal, I'm struggling to get the pages to display in all browsers, the result being I am also unable to view on my phone (Android)
I intend to change to server side processing of the data for display of the web pages.
I hope to then be able to add some basic click buttons to this to turn on/off zones.