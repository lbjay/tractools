#!/bin/bash

TRAC_BASE=/proj/adsset/trac
ENV_BASE=$TRAC_BASE/projects
APP_BASE=$TRAC_BASE/app
PID=$APP_BASE/pid/trac.pid
TRACD=$APP_BASE/python2.6/bin/tracd
PORT=8888
DIGEST_FILE=/proj/adsset/trac/projects/htdigest
EGG_CACHE="PYTHON_EGG_CACHE=/tmp"

ACTION=$1

case $ACTION in
start)
    su -c "$EGG_CACHE $TRACD -d --auth="*",$DIGEST_FILE,ADS --base-path=/trac -e $ENV_BASE \
        --port $PORT --pidfile=$PID" trac 
    ;;
stop)
    kill -9 `cat $PID`
    ;;
*)
    echo "Usage: $0 start|stop"
esac
