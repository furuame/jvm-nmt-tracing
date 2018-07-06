import os
import sys
import time

# JVM pid
PID = sys.argv[1]

# Sampling Period (sec)
interval = 5

# Sampling Times
times = 100

# Temp Output File
tmpfile = "/tmp/tmp-nmt-%d" % (int(time.time()))

# Keywords for each class of memory
keyTotal = "Total"
keyJavaHeap = "Heap"
keyThread = "Thread"
keyGC = "GC"
keyInternal = "Internal"

# JCMD Command
cmdJCMD = "jcmd " + PID + " VM.native_memory"

for i in range(times):
    print("%d / %d" % (i, times))
    os.system(cmdJCMD + " | grep " + keyTotal + " >> " + tmpfile)
    time.sleep(interval)
