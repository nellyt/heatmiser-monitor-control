#
# Neil Trimboy 2011
#

from hm_constants import *

# Master Address
MY_MASTER_ADDR = 0x81

# A list of controllers
# Adjust the number of rows in this list as required
# Items in each row are :
# Controller Address, ShortName, LongName, Controller Type, Graph Colour
StatList = [
[1,  "Study", "Study",    HMV3_ID, "A020F0"],
[2,  "Entrc", "Entrance", HMV3_ID, "D02090"],
[3,  "Dinig", "Dining",   HMV3_ID, "FF4500"],
[4,  "Livig", "Living",   HMV3_ID, "FF8C00"],
[5,  "Kitch", "Kitchen",  HMV3_ID, "FA8072"],
[6,  "Bthrm", "Bathroom", HMV3_ID, "D2691E"],
[7,  "Bed_1", "Bedroom1", HMV3_ID, "FFD700"],
[8,  "M_E_S", "M_E/S",    HMV3_ID, "6B8E23"],
[9,  "Famil", "Family",   HMV3_ID, "32CD32"],
[10, "Laund", "Laundry",  HMV3_ID, "00FA9A"],
[11, "Bed_2", "Bedroom2", HMV3_ID, "1E90FF"],
[12, "Bed_3", "Bedroom3", HMV3_ID, "6A5ACD"],
]

# Named indexing into StatList
SL_ADDR = 0
SL_SHRT_NAME = 1
SL_LONH_NAME = 2
SL_CONTR_TYPE = 3
SL_GRAPH_COL = 4