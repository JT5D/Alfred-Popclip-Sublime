# encoding: utf-8
require 'net/http'
require 'rubygems'
require 'json'
                                                                                       
artist = ENV['POPCLIP_TEXT']
artistt = artist.gsub(' ','+')
  
uri = URI('http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist='+artistt+'&api_key=0746d173dda2f002f61414df72b4a2b6&format=json')
topten = Net::HTTP.get(uri)                         

toptenparsed = JSON.parse(topten)
singles = toptenparsed.fetch("toptracks").fetch("track")
# puts "top 10 singli dla "+artist
for i in (0..9) 
    singles[i]["image"].each { |a| 
    if a["size"]=="extralarge"
    puts "#{i+1}."+singles[i]["name"]   
    puts "[Cover Art]"+"(#{a["#text"]})"
    puts "[Link]"+"(#{singles[i]["url"]})" 
    end                  
    }
end
