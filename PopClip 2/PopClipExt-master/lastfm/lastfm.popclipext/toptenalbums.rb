# encoding: utf-8
require 'net/http'
require 'rubygems'
require 'json'

artist = ENV['POPCLIP_TEXT']
artistt = artist.gsub(' ','+')

uri = URI('http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist='+artistt+'&api_key=0746d173dda2f002f61414df72b4a2b6&format=json')
topten = Net::HTTP.get(uri)                         

toptenparsed = JSON.parse(topten)
albums = toptenparsed.fetch("topalbums").fetch("album")
liczbaalbumow = albums.length
puts "top 10 albumów dla "+artist
for i in (0..9) 
    albums[i]["image"].each { |a| 
    if a["size"]=="extralarge" 
    puts "["+albums[i]["name"]+"]"+"(#{a["#text"]})" 
    end                  
    }
end
 
