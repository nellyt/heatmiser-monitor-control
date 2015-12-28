# How it Works #

A set of controllers is periodically polled.
The current status of each controller (all parameters available) is saved in an xml file.
The current temperatures and on/off status is recorded in a rrd data base
The current temperatures and on/off status for each poll is appended to a csv file

Offline processing can generate graphs from the rrd file
Offline processing can generate a timeline xml file from the csv

The use of a csv file is clunky but was quick to implement. Ideally this will be dropped with only the timeline xml file being modified directly.


# Details #

Add your content here.  Format your content with:
  * Text in **bold** or _italic_
  * Headings, paragraphs, and lists
  * Automatic links to other wiki pages