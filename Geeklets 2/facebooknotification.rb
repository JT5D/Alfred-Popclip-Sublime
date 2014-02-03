# encoding: UTF-8
require 'rss'
require 'net/http'
require 'time'

url=`cat ~/Documents/METRO/CONFIG | grep 'FACEBOOK_URL' | tail -n1 | awk '{print $2}'`
url = url.gsub("\n","")

xURI = URI.parse(url)
	http = Net::HTTP.new(xURI.host, 80)
	request = Net::HTTP::Get.new(xURI.request_uri)
	request['Accept-Language'] = 'en-US,en;q=0.5'
	request['user-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0'
	request['Referer'] = 'http://facebook.com'
	response = http.request(request)
	
x = 0
rss = RSS::Parser.parse(response.body, false, true)
feed = RSS::Parser.parse(rss.to_s)
  	feed.items.each do |item|
    x = x + 1
end
puts x