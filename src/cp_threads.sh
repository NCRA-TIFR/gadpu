#!/bin/bash
#
#Create multiple thread source files for deployment
#
# TODO: Need to directly parse through the exec_thread_file to set the AIPS
#				user ID

i=1
while [ $i -lt 5 ]
do
	cp exec_thread_$i.py exec_thread_$[$i+1].py
	i=$[$i+1]
done

