#!/bin/bash
#
#Create multiple thread source files for deployment
#
# TODO: Need to directly parse through the exec_thread_file to set the AIPS
#				user ID

i=0
while [ $i -lt 5 ]
do
	cp $i'exec'.py $[$i+1]'exec'.py
	i=$[$i+1]
done

