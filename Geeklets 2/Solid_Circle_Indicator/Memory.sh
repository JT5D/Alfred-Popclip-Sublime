#!/bin/bash
username=`whoami`
path="/Users/"${username}"/Documents/Geeklets/Solid_Circle_Indicator"
MEMtotal=`top -l 1 -n 0 | awk '/PhysMem/ {print $8+0 + $10+0}'`
MEMused=`top -l 1 -n 0 | awk '/PhysMem/ {print $2+0 + $4+0}'`
MEMpercent=$(($MEMused * 100 / $MEMtotal))
MEMa5percent=$(($MEMpercent / 5 * 5))
MEMused=`top -l 1 -n 0 | awk '/PhysMem/ {print $8+0}'`
MEMpercent=$(($MEMused * 100 / $MEMtotal))
MEM5percent=$(($MEMpercent / 5 * 5))
cp $path"/Indicator Icons/"${MEM5percent}".png" ${path}"/mem.png"
echo $MEMa5percent " " $MEM5percent
unset username
unset path
unset MEMtotal
unset MEMused
unset MEMpercent
unset MEM5percent
unset MEMa5percent