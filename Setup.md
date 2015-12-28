# Introduction #

Add your content here.


## Source ##


## Download source code ##

## Python ##
Download python2.7
Download pyserial http://pyserial.sourceforge.net/

## RRDTOOL ##

# Optional #
## Web Server ##
## Server side xslt processing ##

# Configuration #

## Email ##
Currently only support Gmail
Put you login and password and where the email is the be sent in email\_settings.py

## Controllers ##
Each controller on your network needs a unique address. This must be done manually at each controller.

Edit stats\_defn.py to contain a list of your controllers
```py

StatList = [
[1,  "Study", "Study",    HMV3_ID, "A020F0", [19,20]],
]
```

Edit stats\_defn.py to contain a list of your circuits
```py

CircuitList = [
[1,  "Bthrm", "Bathroom", [[2.15,2.8],[1.0,1.0]]],
]
```

At first you may want to just have a list of circuits of the same length as there are zones, and set each area to [[1.0.,1.0]]
StatList would then just reference one circuit.
Once things are working you could put the correct data in.

## RS485 ##
Get a working RS485 interface first
This could be onboard, USB or ethernet.
In XXXXX configure the COM port used
```py

serport.port = 6 # 1 less than com port, On mine USB is 6=com7, ether is 9=10
```

## Running for the first time ##
```sh

heating.py
```
This will create several rrd files.
It will also poll each controller.

## Synchronising Time ##
All controllers will be resync'd to the computers time once a day.
Configure your computer with some sort of NTP syncing

Times can be updated manually on all controllers using
```sh

set_time.py
```

## Web Interface ##
Two options
Web pages used to be rendered by the client using a xslt file and the source xml. This does not work on most clients (ie phones).
Server side processing is best.

## Scheduling ##
heating.py is intended to be run every 10 minutes.
parseheating.py should run after heating.py
gen\_graphs.py can be run whenever wanted

# Result #
You should now have time synchronised controllers, polled every 10 minutes.

Web pages will give access to several status pages and links to graphs.

Rarely used features can be access by simple hacks to files such as
  * <pre>hm_lock.py</pre>
  * <pre>hm_set_holiday.py</pre>
## Backup ##
You may want to periodically back up the rrd's