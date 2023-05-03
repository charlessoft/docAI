#!/bin/bash
function stop_name()
 {
 echo "close $1 pid"
     pid=`ps -ef|grep $1|grep -v "grep"|grep -v "stop"|awk '{print $2}'`
         if [ x"$pid" != x"" ]
             then
                 echo "$pid is running...close it!"
                 kill -9 ${pid}
     fi
 }

 stop_name 'textminer/main.py'





