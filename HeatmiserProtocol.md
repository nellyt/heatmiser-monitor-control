# Heatmiser V3 System Protocol #

PRT-EN and PRT\_ENTS controllers use the V3 protocol.


## Documentation Errors ##

_These refer to the V3.0 specification. A newer 3.7 does exists that has not been checked_

There are a few errors and ambiguities in Heatmiser's documentation, mainly in the details of the "DCB structure" that provides the thermostat's configuration and status. The correct details were determined by reverse engineering responses from PRT-EN and PRT-ENTS thermostats and trial and error. Some differences are unresolved. There appear to be more differences with the PRT-**ENTS** controller

  * PRT\_ENTS only : Frost mode (addr 7) is reported differently to spec. Currently unresolved
  * Model (addr 4) : It is not possible to identify a touch screen controller from a non touch-screen controller
  * Current Time (addr 43,44,45,46) Despite the protocol stating that the current day/h/m/s are on 4 separate addresses, tests showed that it was not possible to write to individual values and all 4 values must be written in a single command to addr 43
  * Holiday Hours (addr 24, 25) Despite the protocol stating that the holiday hours are on 2 separate addresses, tests showed that it was not possible to write to individual values and all 2 values must be written in a single command to addr 24

# Other Issues #

  * It is not possible to obtain both the local AND remote temperatures from a unit. A unit is configured to use either the local or remote sensor, the reading for the value not in use is always returned as 0xFFFF, as described in the protocol. This is not significant, but it would be nce to have access to both numbers all the time.
  * The rate of change value on my PRT\_ENTS has been increasing slowly (as expected). It has just got to 255 and seems to have wrapped round to zero. I've no idea of the consequence. Assume this is a software bug in the unit. Support ticket raised with Heatmiser