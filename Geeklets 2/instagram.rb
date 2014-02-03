# encoding: UTF-8
require 'rss'
require 'net/http'
require 'time'



path='/tmp/instagramphoto'
Dir.mkdir(path) unless File.exists?(path)


url=`cat ~/Documents/METRO/CONFIG | grep 'INSTAGRAM_URL' | tail -n1 | awk '{print $2}'`
url = url.gsub("\n","")
xURI = URI.parse(url)
	http = Net::HTTP.new(xURI.host, 80)
	request = Net::HTTP::Get.new(xURI.request_uri)
	request['Accept-Language'] = 'en-US,en;q=0.5'
	request['user-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0'
	request['Referer'] = 'http://facebook.com'
	response = http.request(request)

s = response.body.gsub("<description><![CDATA[","<xxxxxx>")
s = s.gsub("]]></description>","</xxxxxx>")
s = s.gsub("<image>", "\n\n<description><![CDATA[")
s = s.gsub("</image>","]]></description>\n\n")
s = s.gsub("<url>","")
s = s.gsub("</url>","\t")

i = 0

path='/tmp/instagram'

rss = RSS::Parser.parse(s, false, true)
feed = RSS::Parser.parse(rss.to_s)
  	feed.items.each do |item|
  	i = i + 1
    x,y,z = item.description.split(' ') 
    open(x) {|f|
   File.open("/tmp/instagramphoto/#{i}.jpg","wb") do |file|
     file.puts f.read
   end
}
end

