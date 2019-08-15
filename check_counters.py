import glob
import sys

verbose = False

if len(sys.argv) > 1:
    for arg in sys.argv:
        print 'arg=', arg
        if arg == '-v':
            verbose = True

num_counters = 0
#counters = []
counters = {}

counters_h = open("../../../ifaces/counters.h", "r")
for line in counters_h:
    counter_id = line.split()
    if len(counter_id) < 4:
        continue
    if "SSLERR" in counter_id[0]:
        #print '0=',counter_id[0],'1=',counter_id[1],'4=',counter_id[4]
        #counters.append(counter_id[1][:-1])
        counters.update({counter_id[1][:-1]:[False,counter_id[4][:-2]]})
        num_counters += 1

print "There are ", num_counters, "counters in counters.h"
#print counters

path = '*err.h'
files = glob.glob(path)

for fileName in files:
    lib = fileName[:-5]
    if len(lib) < 1:
        continue
    #print fileName
    f = open(fileName, "r")
    if lib == "ssl":
        prefix = ""
        offset = 4
    elif lib == "objects":
        lib = "obj"
        prefix = lib.upper() + "_"
        offset = 0
    else:
        prefix = lib.upper() + "_"
        offset = 0
    libsize = len(lib)
    #print "Library ",lib
    for line in f:
        y = line.split()
        if len(y) > 3 and y[2][:libsize+3] ==  lib.upper() + "_R_":
            reasonCode = prefix + y[2][libsize+3:32 + offset]
            #print reasonCode
            found = False
            for k,v in  counters.items():
                if k == reasonCode:
                    found = True
                    counters.update({k:[True,v[1]]})
                    #print "found a match!", k, "  ",reasonCode
                    break
                if v[1] == prefix + y[2][libsize+3:]:
                    found = True
                    counters.update({k:[True,v[1]]})
                    if verbose:
                        print "found a match with the full reason code - the current counter is", k, "The full name is ",v[1], "the new truncated name would be",reasonCode
                    break
            if not found:
                if  len(reasonCode) >= 30:
                    print "Library",lib,": no counter for ", reasonCode, "possibly due to truncation"
                else:
                    print "Library",lib,": no counter for ", reasonCode
 
num_unused_counters=0
#print counters
for (key,value) in counters.items():
    #print 'key =', key, 'value = ', value
    #print 'type =', type(value[0])
    #print 'type =', type(value[1])
    if value[0] == False:
        if key[:4] != 'LIB_':
            num_unused_counters += 1
            print 'counter ', key,' is unused'

print 'there are ', num_unused_counters, 'unused counters'
