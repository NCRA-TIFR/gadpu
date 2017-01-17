#!/bin/bash

i=11
while [ $i -lt 12 ]
do
	bash -x start_parseltongue.sh exec_thread_1.py $i THREAD_DIR_$[$i]
	i=$[$i+1]
done
