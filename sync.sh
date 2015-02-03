#!/bin/bash
#s sync for webserver
cd /var/www/Website-SST

while true
do
	# "&>/dev/null" silences all echo outputs
	sudo git pull origin master&>/dev/null
	sleep 5
done
