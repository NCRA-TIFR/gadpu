#!/bin/bash

start_parseltongue.sh THREAD11 11 /data2/shubhankar/gadpu/exec_thread_1.py 

if false
then
i=11
while [ $i -lt 12 ]
do
	start_parseltongue.sh THREAD$i/ $vinay ../exec_thread_1.py 
	i=$[$i+1]
done
fi
