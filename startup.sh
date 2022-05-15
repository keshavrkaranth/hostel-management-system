#!/bin/bash
set -e

echo "Starting container..."

python /www/manage.py migrate


# starting gunicorn
GUNICORN=/usr/local/bin/gunicorn
ROOT=/var/www
PID=/var/run/gunicorn.pid
APP=hostelmanagement.wsgi
TIMEOUT=180

if [ -f $PID ]; then rm $PID; fi

cd $ROOT
echo $pwd
echo
# Start your unicorn
exec $GUNICORN -c $ROOT/settings/gunicorn.conf \
    --pid=$PID $APP --timeout=$TIMEOUT &

# starting nginx
service nginx start
