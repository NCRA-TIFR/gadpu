#!/bin/bash
#
# Program to display log files of the running threads


i=0
while true
do
	echo "Iteration" $i
	tail THREAD*.log
	echo '----------------------------------------'
	sleep 1
	i=$[$i+1]
done
