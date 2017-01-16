#!/bin/bash

i=11
while [ $i -lt 17 ]
do
	echo start_parseltongue.sh exec_thread_$i.py $i
	i=$[$i+1]
done
