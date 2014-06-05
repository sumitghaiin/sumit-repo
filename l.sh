DATE=`date +%Y%m%d%H%M%S`; HN=`hostname`; LOAD=`cat /proc/loadavg | awk '{print $1}'`; echo $DATE $HN $LOAD
