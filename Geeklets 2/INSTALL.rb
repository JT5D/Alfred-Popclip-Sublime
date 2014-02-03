#!/usr/bin/ruby

uh = `echo ~`
uh = uh.gsub("\n","")
mp = "#{uh}/Documents/METRO/" 

def wr_f(file_name,data)
  file = File.open(file_name, "w")
  file.puts "#{data}"
  file.close
end

def rd_f(file_name)
  file = File.open(file_name, "r")
  data = file.read
  file.close
  return data
end

fl= <<'TEXT'
CALENDARX_LOGO.glet
CALENDAR_LOGO.glet
CLOCK_LOGO.glet
FACEBOOK_LOGO.glet
INSTAGRAM_LOGO.glet
ITUNES_LOGO.glet
MAIL_LOGO.glet
NETWORK_LOGO.glet
REMINDER_LOGO.glet
RSS_LOGO.glet
SYSTEM_LOGO.glet
TEXT




Dir.glob("#{mp}*_LOGO.glet") do |glf|
  puts "Read #{glf} \n"
	xf = rd_f(glf)
	xf = xf.gsub("<string>file://localhost/Users/xenatt/","<string>file://localhost#{uh}/")
	wr_f(glf,xf)
	puts "Fixed #{glf} \n"
end



