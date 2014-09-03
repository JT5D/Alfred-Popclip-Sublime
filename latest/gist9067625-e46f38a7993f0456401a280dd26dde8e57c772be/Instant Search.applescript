(* Instant Search for LaunchBar by Brett Terpstra
   Requires SearchLink installed in ~/Library/Services (http://brettterpstra.com/projects/searchlink/)
   
   Load the service in LaunchBar and type Space. Enter text, optionally starting with a SearchLink !arg 
   to define the desired search engine. (You do not need the "!!" at the end to specify only url).
  The link will be returned, pressing Enter will open it. ⌘C will copy.
*)on handle_string(message)	set _chars to reverse of characters of message	if (items 1 thru 2 of _chars) as string is not "!!" then		set message to message & "!!"	end if		set myString to do shell script "automator -r -i " & quoted form of message & " ~/Library/Services/SearchLink.workflow|awk '/http/{gsub(/^[ 	]*\"|\"[	 ]*$/,\"\"); print}'"		tell application "LaunchBar"		set selection to myString		remain active	end tellend handle_string