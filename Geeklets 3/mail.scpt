tell application "Mail"
    set theOutput to ""
    repeat with msg in messages in inbox
        if msg's read status is not true then
            set theOutput to theOutput & "• "
        else
            set theOutput to theOutput & "   "
        end if
        set theSender to extract name from sender of msg
        set theSubject to subject of msg
        set theOutput to theOutput & theSender & " – " & theSubject & (ASCII character 10)
    end repeat
    theOutput
end tell