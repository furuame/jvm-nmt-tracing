import os
import sys
import time
from argparse import ArgumentParser
import pandas as pd
import matplotlib.pyplot as plt

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

def askPID():
    program_list = os.popen('jcmd').read()[:-1]
    program_list = program_list.split('\n')
    pid = []
    program = []

    print("Which program do you want to monitor?")
    for i in range(len(program_list)):
        tmplist = program_list[i].split(' ')
        pid.append(tmplist[0])
        print("[%d] %s" % (i, program_list[i]))
    index = int(input())
    return pid[index]

def askTARGET():
    print("Which target do you want to monitor? Ex. \"Total,Heap\"")
    for i in range(len(Target_list)):
        print("[%d] %s" % (i, Target_list[i]))
    ret = input()
    return ret

def ask(name, unit):
    print("Which %s do you want to set? (%s)" % (name, unit))
    ret = input()
    return ret

# Output data as csv file
def output(period, trace, outputfile):
    fout = open(outputfile, "w")
    for i in range(len(trace)):
        fout.write("%d,%s\n" % (i * period, trace[i]))
    fout.close()
    
# plot
def plot(filename, imagename):
    #read csv file
    colnames = ['time', 'Memory Usage']
    data = pd.read_csv(filename, names = colnames)
    
    #plot
    plt.figure(figsize=(20,10), dpi = 72)
    plt.style.use('ggplot')
    plt.plot(data['time'], data['Memory Usage'])
    plt.title('jvm-tracing')
    plt.xlabel('time (sec)')
    plt.ylabel('Memory Usage (KB)')
    plt.grid(True)
    
    #output image
    return plt.savefig(imagename, dpi = 72)

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
    # PID = args.pid
    if args.pid:
        PID = args.pid
    else:
        PID = askPID()

    # Target "list"
    if args.target:
        TARGET = args.target.split(',')
    else:
        TARGET = askTARGET().split(',')

    for tgt in TARGET:
        if tgt not in Target_list:
            print("Target \"%s\" is not availble target" % (tgt))
            quit()

    # Sampling Period (sec)
    if args.period:
        PERIOD = int(args.period)
    else:
        PERIOD = int(ask("Period", "sec"))

    # Sampling Times
    if args.times:
        TIMES = int(args.times)
    else:
        TIMES = int(ask("Sampling Times", "times"))

    # Temp Output File
    tmpfile = "/tmp/tmp-nmt-%d" % (int(time.time()))

    # Output file (csv)
    if args.output_prefix:
        output_prefix = args.output_prefix
    else:
        output_prefix = ask("Output filename prefix", "string")

    tracking(PID, PERIOD, TIMES, tmpfile)
    filtering(tmpfile)

    for tgt in TARGET:
        filename = tmpfile + "-" + tgt
        outputfile = output_prefix + "-" + tgt + ".csv"
        imagename = output_prefix + "-" + tgt + ".png"
        trace = parsing(filename)
        output(PERIOD, trace, outputfile)
        plot(outputfile,imagename)
