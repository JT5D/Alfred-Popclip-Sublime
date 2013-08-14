#!/usr/bin/env ruby
# encoding: utf-8

# myPhoneDesktop for Alfred extension
# v1.1, 09/12/2012
# Author: jProductivity
# Copyright © 2012 jProductivity, LLC
# http://www.myphonedesktop.com/

# visit http://support.myphonedesktop.com/entries/20929458-myphonedesktop-for-alfred-app-extension-send-to-iphone 
# for instructions on how to install and use this extension

# To control how phone number and SMS text will be processed set property AUTO_SEND to "true" or "false"

# "true" - will send selected phone number and SMS text to iPhone and will automatically launch iPhone's Messages.app;
# NOTE: iPhone's Messages.app will auto open only if myPhoneDesktop's iPhone app | Settings | View Options | Auto Respond | SMS option is set to ON

# "false" - will only copy this phone number and SMS text to myPhoneDesktop's desktop client and will not send it to iPhone

# NOTE: in order for AUTO_SEND property to have an effect the USE_DESKTOP_AUTO_SEND_RULES property must be set to "false"

# If AUTO_SEND property is set to either "true" or "false"
# it will override all "Auto Send" options set in "Phone Options" of myPhoneDesktop's desktop client.
# You can control this by setting USE_DESKTOP_AUTO_SEND_RULES property to "true" or "false".
# If USE_DESKTOP_AUTO_SEND_RULES property is set to "true" then script will honor all "Auto Send" options set in
# "Phone Options" of myPhoneDesktop's desktop client


APP_NAME = "mpd"
APP_PATH = "/Applications/myPhoneDesktop.app"
USE_DESKTOP_AUTO_SEND_RULES = true
AUTO_SEND = true

def mpd_installed?
  File.exist?("#{APP_PATH}") ? true : false
end

def mpd_running?(app_name)
  `ps aux` =~ /#{app_name}/ ? true : false
end

def can_send_to_mpd?
  unless mpd_installed?
    `osascript -e 'tell application "System Events"' -e 'display dialog "There is no myPhoneDesktop installed on your computer. Visit the myPhoneDesktop site to download and install myPhoneDesktop on your computer, iPhone, iPad or iPod touch." with title "myPhoneDesktop is not installed" with icon 2 buttons {"OK"} default button 1' -e 'open location "http://www.myphonedesktop.com/"' -e 'end tell'`
    puts "myPhoneDesktop extension for Alfred :: myPhoneDesktop is not installed! Download from http://www.myphonedesktop.com/"
    Process.exit
  end

  unless mpd_running?("myPhoneDesktop.app")
    `open -a \"#{APP_PATH}\"`
    sleep(5)
  end
  mpd_running?("myPhoneDesktop.app")
end

def is_phone?
  #get data before the pipe
  result = ARGV[0].split(/\|/i)

  #Strip all chars except alphanumeric and +
  clean_phone_number = result[0].gsub(/[^0-9a-z\+]/i, '')

  #Check if first parameter is the phone number matching NANP Format
  # NANP Format: http://www.nanpa.com/about_us/abt_nanp.html
  nanp_format = clean_phone_number =~ /\A(?:(?x)^((\*?|\#?)[0-9]+\#{1})?(?:\+?1[-.\x20]?)?\(?([2-9][0-8][0-9])\)?[-.\x20]?([2-9][0-9]{2})[-.\x20]?([0-9]{4})$)\Z/i ? true : false

  # Check if first parameter is the phone number matching N11 Format
  # http://en.wikipedia.org/wiki/N11_code
  n11_format = clean_phone_number =~ /\A(?:(?x)^(?:\+?(?:211|311|411|511|611|711|811|911))$)\Z/i ? true : false

  # Check if first parameter is the phone number matching Generic International Format
  international_format = clean_phone_number =~ /\A((?x)^((\*?|\#?)[0-9]+\#{1})?\+(?:[0-9]\x20?){6,14}[0-9]$)\Z/i ? true : false

  # Check if first parameter is the phone number matching format of Vanity numbers in the United States
  #http://en.wikipedia.org/wiki/Phoneword#Vanity_numbers_in_the_United_States
  vanity_format = clean_phone_number =~ /\A(?:(?x)^((\*?|\#?)[0-9]+\#{1})?(?:\+?1[-.]?)?\(?(800|888|877|866|855|844|833|822|880|887|889)\)?([-.0-9a-z]{7,})$)\Z/i ? true : false

  nanp_format || n11_format || international_format || vanity_format ? true : false
end

def is_sms?
  ARGV[0] =~ /\|/i ? true : false
end

def process_query(data)
  is_file = File.exist?(data) && ! File.directory?(data)

  allowed_image_files = [".jpeg", ".jpg", ".png", ".gif"]
  allowed_text_files = [".text", ".txt", ".js", ".log", ".css", ".vcf", ".htm", ".html", ".md", ".markdown", ".rb", ".sql", ".java", ".csv", ".htm", ".html"]

  if is_file
    file_name = File.basename("#{data}")
    file_kind = File.extname("#{data}")

    if allowed_image_files.include?(file_kind) || allowed_text_files.include?(file_kind)
      t = Thread.new do
        `osascript -e 'set the clipboard to POSIX file "#{data}"'`
      end
      t.join
    else
      `osascript -e 'tell application "System Events"' -e 'display dialog "myPhoneDesktop unable to process file:" & return & return & "#{File.basename(data)}" & return & return & "Supported file types include text files (txt, vCard, markdown, etc.) and images (gif, jpeg and png)" with title "Unsupported File Type" with icon 2 buttons {"OK"} default button 1' -e 'end tell'`
      puts "myPhoneDesktop extension for Alfred :: Unsupported File Type. myPhoneDesktop is not able to process " + file_kind + ": " + File.basename(data)
      Process.exit
    end

  else
    if is_phone? && is_sms? then
      if USE_DESKTOP_AUTO_SEND_RULES then
        data = "${command=phoneSMS}|#{data}"
      else
        data = "${command=phoneSMS; autoSend=#{AUTO_SEND}}|#{data}"
      end
    end

    data = data.gsub(/["]/i, '\\"')
    t = Thread.new do
      `osascript -e 'set the clipboard to "#{data}" as Unicode text'`
    end
    t.join
  end

  send_to_mpd
end

def send_to_mpd
  `osascript -e 'tell application "System Events"' -e 'key code 113 using {shift down, control down, option down, command down}' -e 'end tell'`
end

def help
  puts "myPhoneDesktop extension for Alfred :: Missing required parameter"
  puts "Usage: #{APP_NAME} [phone, text, file]"
end

if ARGV.size == 0
  help
else
  if can_send_to_mpd?
    process_query(ARGV[0].strip)
  else
    puts "myPhoneDesktop extension for Alfred :: myPhoneDesktop is not running. Unable to send data to myPhoneDesktop"
  end
end
