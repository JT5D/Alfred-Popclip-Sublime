WEATHER CONDITIONS (must be personalised)



curl --silent "http://weather.yahooapis.com/forecastrss?p=CAXX0236&u=c" | grep -E '(Current Conditions:|C<BR)' | tail -n1 | sed -e 's///' -e 's/ C$/˚C/'



Refresh Rate: 600





Simply replace



CAXX0236&u=c



with your own city's address





***The final letter c in "CAXX0236&u=c" refers to celsius, so replacing it to the letter"f" makes it fahrenheit



HOW TO:

- go to : weather.yahoo.com/

- find your city's weather page by searching it

- click on the rss feed button (it's orange and says RSS...)

- the last part of the webpage's address is what you need to replace my own code above



*****************************************************



WEATHER IMAGE FETCHER (must be personalized)



create an empty shell with this code:



curl --silent -o /tmp/weather.html ca.weather.yahoo.com/canada/quebec/longueuil-4388/;



Refresh rate: 600

*Fetches image from yahoo server and store it locally.*





Simply replace



ca.weather.yahoo.com/canada/quebec/longueuil-4388/



with your own city's address





HOW TO:

- go to : weather.yahoo.com/

- find your city's weather page by searching it

- the last part of the webpage's address is what you need to replace my own code above



*****************************************************



DATE



date "+%a, %B %d"



Refresh rate: 1000



*****************************************************



TIME



date "+%l:%M"



Refresh rate: 20



*****************************************************



UPTIME



uptime | sed 's/.* up /Uptime: /' | sed s/,.*//;



Refresh rate: 60

*There is a better uptime code but I can't find it right now so I'll post it on my next geektools desktop.*





**********************************************************************************************************