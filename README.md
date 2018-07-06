# jvm-nmt-tracing

## Introduction

This project can give you the internal memory usage of Java Virtual Machine (JVM) via Native Memory Tracking (NMT) feature offered by Java7U40 later version.



## Prerequisites

* OpenJDK8 or later version

* Python3

* Launch your Java program by enable NMT feature.

  ```shell
  $ java -XX:NativeMemoryTracking=summary <launch program>
  ```

* Then get the `<PID>` of this java program via `jcmd`

  ```shell
  $ jcmd
  ```

  

## Start tracing

* Launch the tracing program

  ```shell
  $ python3 tracing.py --pid <java program pid> \
                       --target <Target Class of Memory> \
                       --period <Sampling period in sec> \
                       --times <Times of Sampling> \
                       --output <Output file in csv>
  ```

* Classes of internal memory in JVM

  * `Total` Committed Memory
  * Java `Heap` Committed Memory
  * `Thread` Committed Memory
  * Garbage Collection (`GC`) Committed Memory
  * `Internal` Committed Memory

* For example, if I want to track the GC memory usage of the given java progam (pid = 9527) every 5 sec, total 100 times, and recored in `./output.csv` file

  ```shell
  $ python3 tracing.py --pid 9527 \
                       --target GC \
                       --period 5 \
                       --times 100 \
                       --output ./output.csv
  ```

* Output file is like the following

  ```
  < time (sec), Memory Usage (KB) >
  0,2318027
  5,3478519
  10,3587211
  15,3651405
  20,3650761
  25,3658298
  30,3625863
  35,3630655
  40,3716090
  ```

  

## Licensing

`jvm-nmt-tracing` is freely redistributable under  the MIT License. Use of this source code is governed by a MIT-style  license that can be found in the `LICENSE` file. 