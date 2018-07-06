import os
import sys
import time

# Keywords for each class of memory
Target_list = ["Total", "Heap", "Thread", "GC", "Internal"]

# Tracking <target> <times> Process <pid> every <period> sec
def tracking(pid, target, period, times, tmpfile):
    cmdJCMD = "jcmd " + pid + " VM.native_memory"

    for i in range(times):
        # os.system(cmdJCMD + " | grep " + target + " >> " + tmpfile)
        print(cmdJCMD + " | grep " + target + " >> " + tmpfile)
        time.sleep(period)

if __name__ == "__main__":
    # JVM pid
    # TODO: Handling invlaid PID
    PID = sys.argv[1]

    # Target
    TARGET = sys.argv[2]
    if TARGET not in Target_list:
        print("Not Available Target")
        quit()

    # Sampling Period (sec)
    PERIOD = int(sys.argv[3])

    # Sampling Times
    TIMES = int(sys.argv[4])

    # Temp Output File
    tmpfile = "/tmp/tmp-nmt-%d" % (int(time.time()))

    tracking(PID, TARGET, PERIOD, TIMES, tmpfile)
