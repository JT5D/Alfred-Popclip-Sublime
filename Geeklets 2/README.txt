
-----------------------------------------------------------------------------------

INSTALLATION GUIDE

-----------------------------------------------------------------------------------

1. Copy METRO folder to <Home Folder>/Documents/ (aka look like /Users/xxx/Documents/METRO)

2. Run 'ruby ~/Documents/METRO/INSTALL.rb' without qoute in terminal
3. Edit CONFIG FILE (~/Documents/METRO/CONFIG) READ CONFIG SECTION
4. open ~/Documents/METRO/BACKGROUND and open glet file 
5. open ~/Documents/METRO/ open INSTAGRAM_SLIDE.glet first and All else other glet



-----------------------------------------------------------------------------------

CONFIG GUIDE

-----------------------------------------------------------------------------------

METRO Geeklets is glet modifiedless for config.
You config this geeklets without modify glet file.
But you must edit Config File (~/Documents/METRO/CONFIG)
You must see text like this.I will tell you what's mean,How to config.
Config file write by Tab (Space) pattern aka


CONFIG_KEY(TAB KEY)CONFIG_VALUE

like this……

#WERATHER CITY key not use in metro geeklets But you can put one without space key

WEATHER_CITY	Kuraburi,Thailand

#WEATHER CODE key you can get this form http://weather.yahoo.com
and copy city code to Config value like

WEATHER_CODE	THXX0024	

#WEATHER Formatt We use different formatt. celsius and fahrenheit
if you use fahrenheit edit WEATHER_FORMATT like this

WEATHER_FORMATT f

if celsius use

WEATHER_FORMATT c

#Weather theme you can change weather icons theme by edit value 
This value form Weather theme folder ~/Documents/METRO/Weather/

WEATHER_THEME	White

#iTunes theme you can change iTunes Player Stat theme by edit value 
This value form iTune theme folder ~/Documents/METRO/itunes/

ITUNES_THEME	Default

#RSS URL this notify you when have new topic form web site you like to read this

RSS_URL	http://lifehacker.com/rss

#RSS Name Naming your rss notify
RSS_NAME	Lifehacker

#Facebook notify you must visit https://www.facebook.com/notifications 
You will see RSS link , copy url to config key
FACEBOOK_URL https://www.facebook.com/feeds/notifications.php?blablabla	

#Instagram slide you easy config put user name on this url like

INSTAGRAM_URL	http://widget.stagram.com/rss/n/[username]


DO NOT ADD OTHER LINE TO CONFIG FILE 