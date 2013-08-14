 #!/bin/sh
 #Screen Sharing for Alfred
 #Version 1.1
 #Developer: Don Southard aka @binaryghost
 #January 19, 2012

#Main function for prompting user to choose a host
getSelectedServer() {
osascript <<EOS
	tell application "Finder"
		activate
		set theList to {}
		set theFile to the POSIX path of "$1"
		set Names to paragraphs of (read theFile)
		repeat with nextLine in Names
			if length of nextLine is greater than 0 then
				copy nextLine to the end of theList
			end if
		end repeat
		set selectedServer to choose from list theList with prompt "Please select a host: " with title "Screen Sharing for Alfred" OK button name "$2" without multiple selections allowed
		return selectedServer
	end tell
EOS
}

#Function to collect info for adding a host to the list
getServerInfo() {
osascript <<EOS
	tell application "Finder"
		activate 
		set theInput to the text returned of (display dialog "Please enter the $1 of the host" with title "Screen Sharing for Alfred" default answer "")
		return theInput 
	end tell
EOS
}

#Function for confirmation on killall command
confirmation() {
osascript <<EOS
	tell application "Finder"
		activate
		set theChoice to display dialog "Are you sure you want to remove ALL connections?"  with title "Screen Sharing for Alfred" buttons {"Cancel", "Remove"} default button 1
		return theChoice
	end tell
EOS
}		

#Input query from Alfred
INPUT="$1"

#Add query to array
declare -a array=($INPUT)

#Parse out first item, it is the todo command
COMMAND=`echo "${array[0]}" | tr A-Z a-z`

#Get the file path of addresses config file
addressFile=$(echo "`pwd`/addresses.txt")

#Get the file path of addresses config file
namesFile=$(echo "`pwd`/names.txt")

#Add a host to the connections list
if [[ $COMMAND = 'add' || $COMMAND = 'setup' ]]
then
	#Call function to collect name/address from user
	ServerName=`getServerInfo "name"`
	ServerAddress=`getServerInfo "address"`

	#Make sure both the name and address have values
	if [ ! -z "$ServerName" ] && [ ! -z "$ServerAddress" ]
	then
		echo "$ServerName" >> names.txt
		echo "$ServerName:$ServerAddress" >> addresses.txt
		echo "Added $ServerName to your list of connections"
	fi
	exit
fi

#Display About
if [ $COMMAND = 'about' ]
then
	cat about.txt
	exit
fi

#Display Help Window
if [ $COMMAND = 'help' ]
then
	cat help.txt
	exit
fi

#Display Changelog Window
if [ $COMMAND = 'changelog' ]
then
	cat changelog.txt
	exit
fi

#Display Version Number
if [ $COMMAND = 'version' ]
then
	version=$(cat update.xml | grep -Po '(?<=<version>)\d.\d(?=</version>)')
	echo "Version "$version
	exit
fi

#Check address file to see if it is empty
if [ ! -s "$addressFile" ]
then
	echo "Please run the 'add' command first"
	exit
fi

#Remove a host connection from list
if [[ $COMMAND = 'rm' || $COMMAND = 'remove' ]]
then
	selectedServer=`getSelectedServer "$namesFile" "Remove"`
	if [ "$selectedServer" != "false" ]
	then
		sed -i "" "/$selectedServer/d" names.txt
		sed -i "" "/^$selectedServer/d" addresses.txt
		echo "Removed $selectedServer to the client"
	fi
	exit
fi

#Remove ALL connections from the host list
if [[ $COMMAND = 'killall' ]]
then
	kill=`confirmation`
	if [[ "$kill" = "button returned:Remove" ]]; then
		> names.txt
		> addresses.txt
		echo "All stored connections have been removed"
	fi
	exit
fi

#List all currently stored connections
if [[ $COMMAND = 'ls' || $COMMAND = 'list' ]]
then
	echo "All Stored Connections:"
	cat addresses.txt | sed 's/:/ - /g'
	exit
fi

#Simply open the Screen Sharing.app for quick VNC session
if [[ $COMMAND = 'open' ]]
then
	/System/Library/CoreServices/Screen\ Sharing.app/Contents/MacOS/Screen\ Sharing
	exit
fi

#Connect to a selected host
if [[ $COMMAND = 'connect' ]]
then

	selectedServer=`getSelectedServer "$namesFile" "Connect"`
	if [ "$selectedServer" != "false" ]
	then
		
		#Parse out the address from the return
		SERVERADDRESS=$(cat addresses.txt | grep "$selectedServer" | awk 'BEGIN { FS = ":" } ; { print $2 }')

		#open a vnc connection
		open "vnc://$SERVERADDRESS"
	fi
fi
