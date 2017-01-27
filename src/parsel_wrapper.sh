#!/bin/bash
#
# Launches multiple threads for execution. The ParselTongue start file has been
# edited to support the non-interactive nature of the application.

i=11
while [ $i -lt 16 ]
do
	start_parseltongue.sh THREAD$i/ $i ../exec_thread_$[$i-10].py &> THREAD$i.log &
	i=$[$i+1]
done
