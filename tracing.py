import os
import sys
import time
from argparse import ArgumentParser

# Keywords for each class of memory
Target_list = ["Total", "Heap", "Thread", "GC", "Internal"]

# Tracking <times> Process <pid> every <period> sec
def tracking(pid, period, times, tmpfile):
    cmdJCMD = "jcmd " + pid + " VM.native_memory"

    for i in range(times):
        os.system(cmdJCMD +  " >> " + tmpfile)
        # print(cmdJCMD + " | grep " + target + " >> " + tmpfile)
        print("Progress : %d / %d" % (i, times))
        time.sleep(period)

# Filtering each target on timpfile
def filtering(tmpfile):
    fin = open(tmpfile, "r")
    trace = []
    while True:
        line = fin.readline()
        if not line: break
        trace.append(line)
    fin.close()

    for tgt in Target_list:
        fout = open(tmpfile + "-" + tgt, "w")
        for line in trace:
            if tgt in line: fout.write(line)
        fout.close()

# Parsing statistic data from specific file
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
    parser.add_argument("--output-prefix", dest = "output_prefix")
    args = parser.parse_args()

    # JVM pid
    # TODO: Handling invlaid PID
    PID = args.pid

    # Target "list"
    TARGET = args.target.split(',')

    # Sampling Period (sec)
    PERIOD = int(args.period)

    # Sampling Times
    TIMES = int(args.times)

    # Temp Output File
    tmpfile = "/tmp/tmp-nmt-%d" % (int(time.time()))

    # Output file (csv)
    output_prefix = args.output_prefix

    tracking(PID, PERIOD, TIMES, tmpfile)
    filtering(tmpfile)

    for tgt in TARGET:
        if tgt not in Target_list:
            print("%s is not availble target" % (tgt))
            pass
        filename = tmpfile + "-" + tgt
        outputfile = output_prefix + "-" + tgt + ".csv"
        trace = parsing(filename)
        output(PERIOD, trace, outputfile)
