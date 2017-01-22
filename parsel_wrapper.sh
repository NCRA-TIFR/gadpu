#!/bin/bash

#start_parseltongue.sh THREAD11 11 /data2/shubhankar/gadpu/exec_thread_1.py 

i=11
while [ $i -lt 16 ]
do
	start_parseltongue.sh THREAD$i/ $i ../exec_thread_$[$i-10].py &> THREAD$i.log &
	i=$[$i+1]
done
