# Weather:

curl --silent "http://xml.weather.yahoo.com/forecastrss?p=29301&u=f" | grep -e "Current Conditions" -A 1 | tail -n 1 | sed -e 's/<BR \/>//' && echo && curl --silent "http://xml.weather.yahoo.com/forecastrss?p=29301&u=f" | grep -e "Forecast:" -A 2 | tail -n 2 | sed -e 's/<br \/>//' -e 's/<BR \/>//' | sed "s/\(.*\)\.\ \(.*\)/\1\?\2/" | tr "?" "\n" | sed "s/High\:\ \(.*\)\ Low\:\ \(.*\)/\?H\: \1\ L\:\ \2/" | sed "s/\?\(.*\)/\\1/"



# Remind:

/opt/local/bin/rem | sed s/Reminders\ for\ .*/Reminders\ for\ today./



# Top (sort by cpu);

top -ocpu -l2 -n10 -p "^bbbbbbbbbbbb  \$ccccc" -P "Command           CPU" | tail -n11 | grep -v top



# Top (sort by rsize):

top -orsize -l2 -n10 -p "^bbbbbbbbbbbb  \$jjj" -P "Command         MEM" | tail -n11 | grep -v top



# Top (sort by vsize)

top -ovsize -l2 -n10 -p "^bbbbbbbbbbbb  \$lll" -P "Command        VMEM" | tail -n11 | grep -v top



# Uptime, Memory Usage and Ram Usage (use align right)

top -l 1 | awk '/PhysMem/ {print $8 " : RAM"}'; top -l1 | grep "CPU usage:" | sed 's/.*\(CPU .*\)\ user.*/\1/' | awk '{print $3 " : " $1}'; uptime | awk '{print $3 " " $4 " " $5 " : UPTIME" }' | sed 's/\(.*\)\,/\1/'



# Fetches Weather Image to /tmp/weather.png
# add a image setting in geektool to display the image: file:///tmp/weather.png

curl --silent "http://rss.weather.com/weather/rss/local/10003?cm_ven=LWO&cm_cat=rss&par=LWO_rss" | grep "forecast-icon" | sed "s/.*background\:url(\'\(.*\)\')\;\ _background.*/\1/" | xargs curl --silent -o /tmp/weather.png



#External IP:

echo "E: " `curl --silent http://checkip.dyndns.org | awk '{print $6}' | sed "s/\(.*\)\<\/body\>\<\/html\>/\1/"`



#Internal IP:

echo "I: " `ifconfig en1 | grep inet | grep -v inet6 | awk '{print $2}'`