#!/bin/bash
username=`whoami`
path="/Users/"${username}"/Documents/Geeklets/Hashed_Circle_Indicator"
DISKpercent=`df -h | awk '/disk0s2/ {print $5+0}'`
DISK17=$(($DISKpercent * 4 / 25 + 1))
cp $path"/Indicator Icons/"${DISK17}".png" ${path}"/disk.png"
echo "/    " $DISKpercent
unset username
unset path
unset DISKpercent
unset DISK17