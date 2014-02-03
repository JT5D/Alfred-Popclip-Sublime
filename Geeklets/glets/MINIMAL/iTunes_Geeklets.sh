theme=`echo Default`
itnsps=`osascript -e "tell application \"System Events\"" -e "if (exists application process \"iTunes\") then" -e "return \"yes\"" -e "else" -e "return \"no\"" -e "end if" -e "end tell"`
lasttrack=`tail /tmp/itunestrack`


if [ "$itnsps" = "yes" ] 
then 
itnsplst=`osascript -e "tell application \"iTunes\"" -e "return (get player state as string)" -e "end tell"`

		if [ "$itnsplst" = "playing" ] 
		then
			track=`osascript -e "tell application \"iTunes\"" -e "set curTrack to current track" -e "name of curTrack as string" -e "end tell"`
			album=`osascript -e "tell application \"iTunes\"" -e "set curTrack to current track" -e "album of curTrack as string" -e "end tell"`
			artist=`osascript -e "tell application \"iTunes\"" -e "set curTrack to current track" -e "artist of curTrack as string" -e "end tell"`
			itnesstat=`osascript -e "tell application \"iTunes\"" -e "set trackname to name of current track" -e "set trackduration to duration of current track" -e "set trackposition to player position" -e "set elapsed to round (trackposition / trackduration * 100)" -e "set output to elapsed" -e "end tell"`
			if [ "$track" != "" ]
				then
					echo $track
					if [ "$album" != "" ]
					then
						echo $album	
					else 
						echo "UNKNOW"
					fi
					if [ "$artist" != "" ]
					then
						echo $artist
					else 
						echo "UNKNOW"
					fi
				fi
			playtrack=`echo $track-$artist-$album`;
			if [ "$lasttrack" != "$playtrack" ]
			then
				echo $track-$artist-$album > /tmp/itunestrack
				osascript -e "set myPath to ((path to home folder) as text) & \"Documents:\" & \"MINIMAL:\" & \"iTunes:\"" -e "set artworkItunes to POSIX path of myPath & \"iTunes-Cover.png\"" -e "set defaultPic to POSIX path of myPath & \"default.png\"" -e "tell application \"iTunes\"" -e "set artData to data of artwork 1 of current track" -e "set fileRef to (open for access artworkItunes with write permission)" -e "try" -e "write artData to fileRef starting at 0" -e "close access fileRef" -e "on error" -e "try" -e "close access fileRef" -e "end try" -e "error" -e "end try" -e "end tell"
				if [ -f ~/Documents/MINIMAL/iTunes/iTunes-Cover.png ]
				then
 					mv ~/Documents/MINIMAL/iTunes/iTunes-Cover.png /tmp/iTunes-Cover.png
				else 
 					ln -sf ~/Documents/MINIMAL/iTunes/$theme/default.png /tmp/iTunes-Cover.png
				fi
			fi
			if [[ "$itnesstat" -ge 0 && "$itnesstat" -lt 5 && "$itnesstat" != "" ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/0.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 5 && "$itnesstat" -lt 10 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/5.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 10 && "$itnesstat" -lt 15 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/10.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 15 && "$itnesstat" -lt 20 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/15.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 20 && "$itnesstat" -lt 25 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/20.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 25 && "$itnesstat" -lt 30 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/25.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 30 && "$itnesstat" -lt 35 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/30.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 35 && "$itnesstat" -lt 40 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/35.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 40 && "$itnesstat" -lt 45 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/40.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 45 && "$itnesstat" -lt 50 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/45.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 50 && "$itnesstat" -lt 55 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/50.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 55 && "$itnesstat" -lt 60 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/55.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 60 && "$itnesstat" -lt 65 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/60.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 65 && "$itnesstat" -lt 70 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/65.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 70 && "$itnesstat" -lt 75 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/70.png /tmp/iTunes-stat.png
				elif [[ "$itnesstat" -ge 75 && "$itnesstat" -lt 80 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/75.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 80 && "$itnesstat" -lt 85 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/80.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 85 && "$itnesstat" -lt 90 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/85.png /tmp/iTunes-stat.png
			elif [[ "$itnesstat" -ge 90 && "$itnesstat" -lt 95 ]]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/90.png /tmp/iTunes-stat.png
			else
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/95.png /tmp/iTunes-stat.png
			fi

		else
			if [ "$lasttrack" != "" ]
			then
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/empty.png /tmp/iTunes-Cover.png
				ln -sf ~/Documents/MINIMAL/iTunes/$theme/1.png /tmp/iTunes-stat.png
				echo "" > /tmp/itunestrack
			fi
		fi
		
else
	if [ "$lasttrack" != "" ]
	then
		ln -sf ~/Documents/MINIMAL/iTunes/$theme/empty.png /tmp/iTunes-Cover.png
		ln -sf ~/Documents/MINIMAL/iTunes/$theme/1.png /tmp/iTunes-stat.png
		echo "" > /tmp/itunestrack
	fi
fi
