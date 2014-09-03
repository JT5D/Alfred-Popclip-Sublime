activate application "Sublime Text"

tell application "System Events" to keystroke "n" using command down
tell application "System Events" to keystroke "v" using command down
tell application "System Events" to keystroke "s" using command down

tell application "System Events"
	tell process "Sublime Text"
		set theDate to current date
		set moo to (day of theDate) + (month of theDate) + (year of theDate) + (time of theDate)
		set dat to moo
		keystroke dat
		keystroke return
	end tell
end tell
--tell process "Finder"



--click menu item "Paste" of menu 3
--end tell


