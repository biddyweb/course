#!/bin/sh -e

COURSE_DIR=/var/local/course
USER=course
GROUP=course

case "$1" in
  start)
    paster serve --daemon --user=${USER} --group=${GROUP} --pid-file=${COURSE_DIR}/paster.pid --log-file=${COURSE_DIR}/paster.log ${COURSE_DIR}/production.ini start
    ;;
  stop)
    paster serve --daemon --user=${USER} --group=${GROUP} --pid-file=${COURSE_DIR}/paster.pid --log-file=${COURSE_DIR}/paster.log ${COURSE_DIR}/production.ini stop
    ;;
  restart)
    paster serve --daemon --user=${USER} --group=${GROUP} --pid-file=${COURSE_DIR}/paster.pid --log-file=${COURSE_DIR}/paster.log ${COURSE_DIR}/production.ini restart
    ;;
  *)
    echo $"Usage: $0 {start|stop|restart}"
    exit 1
esac
