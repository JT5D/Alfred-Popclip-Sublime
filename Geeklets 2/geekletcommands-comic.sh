Top Processes

top -FR -l2 -o cpu | grep -v 0.0% | cut -c 7-24| sed -n '15, $p'



Time

date "+%l:%M"



AM & PM

date +%p



Date Number

date +%d



Month

date +%B



Weekday

date +%A



Calendar

cal



To Do List

Create a text file with TextEdit but make sure you click Format>Make Plain Text before save. Then select the file in path in GeekTool.



Uptime

uptime | awk '{print "" $3 " " $4 " " $5 }' | sed -e 's/.$//g';



RAM

top -l 1 | awk '/PhysMem/ {print "" $8 " "}' ;



CPU

top -l 2 | awk '/CPU usage/ && NR > 5 {print $12, $13}'



Hard Drive Space

df -h | grep disk0s2 | awk '{print $4 }'