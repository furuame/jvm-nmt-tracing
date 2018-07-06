import os
import sys
import time
from argparse import ArgumentParser

# Keywords for each class of memory
Target_list = ["Total", "Heap", "Thread", "GC", "Internal"]

# Tracking <target> <times> Process <pid> every <period> sec
def tracking(pid, target, period, times, tmpfile):
    cmdJCMD = "jcmd " + pid + " VM.native_memory"

    for i in range(times):
        os.system(cmdJCMD + " | grep " + target + " >> " + tmpfile)
        # print(cmdJCMD + " | grep " + target + " >> " + tmpfile)
        print("Progress : %d / %d \n" % (i, times))
        time.sleep(period)

# Parsing statistic data from tmpfile
def parsing(tmpfile):
    # The target string : "committed=123456KB"
    trace = []
    fin = open(tmpfile, "r")
    while True:
        line = fin.readline()
        if not line: break
        line = line.split("committed=")[1]
        line = line.split("KB")[0]
        trace.append(line)
    fin.close()
    return trace

# Output data as csv file
def output(period, trace, outputfile):
    fout = open(outputfile, "w")
    for i in range(len(trace)):
        fout.write("%d,%s\n" % (i * period, trace[i]))
    fout.close()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--pid", dest = "pid")
    parser.add_argument("--target", dest = "target")
    parser.add_argument("--period", dest = "period")
    parser.add_argument("--times", dest = "times")
    parser.add_argument("--output", dest = "output")
    args = parser.parse_args()

    # JVM pid
    # TODO: Handling invlaid PID
    PID = args.pid

    # Target
    TARGET = args.target
    if TARGET not in Target_list:
        print("Not Available Target")
        quit()

    # Sampling Period (sec)
    PERIOD = int(args.period)

    # Sampling Times
    TIMES = int(args.times)

    # Temp Output File
    tmpfile = "/tmp/tmp-nmt-%d" % (int(time.time()))

    # Output file (csv)
    outputfile = args.output

    tracking(PID, TARGET, PERIOD, TIMES, tmpfile)
    trace = parsing(tmpfile)
    output(PERIOD, trace, outputfile)
