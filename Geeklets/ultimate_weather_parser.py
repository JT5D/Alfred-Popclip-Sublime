#!/usr/bin/env python

""" ULTIMATE WEATHER PARSER BETA 03
 ROBERT WOLTERMAN (xtacocorex) - 2012

 GRABS THE WEATHER FROM THE WEATHER SITE OF YOUR CHOOSING SO YOU CAN DISPLAY IT ON
 YOUR DESKTOP WITH GEEKTOOL/NERDTOOL
 
 SITES SUPPORTED:
 - YAHOO WEATHER
 - WEATHER UNDERGROUND
 - US NATIONAL WEATHER SERVICE
 
 LOCATION GRABBING:
  - SUPPORTED AND CAN BE PULLED FROM THE FOLLOWING SITE
    - http://ipinfodb.com/my_ip_location.php
 
 WEATHER IMAGE AUTOMATIC DOWNLOAD:
  WEATHER IMAGES ARE AUTOMATICALLY DOWNLOADED WHEN THE SCRIPT IS RUN
  IMAGES ARE STORED IN /tmp, THIS IS CUSTOMIZABLE WITH THE IMAGESAVELOCATION VARIABLE
  IMAGE TYPES:
   - YAHOO! -> 
       CURRENT:          yahoo_current_wx.gif
       TWO DAY:          yahoo_fcast_day1.gif & yahoo_fcast_day2.gif
       FIVE DAY:         NOT SUPPORTED
   - WEATHER.COM ->
       CURRENTLY NOT IMPLEMENTED
   - WUNDERGROUND ->
       CURRENT:          wunderground_current_wx.gif
       MULTI-DAY:        wunderground_fcast_dayX.gif WHERE X IS 1 TO NUMBER OF DAYS YOU SET
   - WEATHERBUG ->
       CURRENTLY NOT IMPLEMENTED
   - NATIONAL WEATHER SERVICE ->
       CURRENT:          NOT SUPPORTED
       MULTI-DAY SIMPLE: usnws_fcast_dayX
 
 ********************************************************************************
 I DO NOT RECOMMEND RUNNING MULTIPLE INSTANCES OF THIS SCRIPT TO OUTPUT DIFFERENT
    SETS OF DATA - THIS IS A COMPLEX SCRIPT THAT WILL EAT UP SYSTEM RESOURCES
 ********************************************************************************
 
 *** MAKE SURE TO SET THE REFRESH RATE IN GEEKTOOL/NERDTOOL TO A REASONABLE VALUE
"""

# CHANGELOG
# 22 APRIL 2012
#  - CURRENTLY REMOVED SUPPORT FOR WEATHER CHANNEL AND ACCUWEATHER - RELEASING AS BETA 03
# 21 APRIL 2012
#  - EXTRACTED ALL THE CLASSES AND DATA INTO SEPARATE FUNCTIONS FOR EASE OF EXPANSION
#    - THIS WILL MAKE INSTALLATION MORE DIFFICULT THOUGH, BUT THIS IS FOR GEEKTOOL...
# 07 JANUARY 2012
#  - INITIAL WRITE

# MODULE IMPORTS
import  os, sys, optparse
# forecasts HOLDS THE Forecasts AND FCDay CLASSES
import forecasts
# location HOLDS THE Location and IPINFODB CLASS
import location
# globals HOLDS ALL OF THE GLOBAL VARIABLES FOR THE SCRIPT
from globals                    import *
# utilityfunctions HOLDS ALL THE MISCELLANEOUS FUNCTIONS NEEDED FOR OPERATION
from utilityfunctions           import *

# IMPORT THE WEATHER SERVICES
from services.wx_yahoo          import YahooWeather
#from services.wx_weatherchannel import WeatherChannel
from services.wx_wunderground   import WeatherUnderground
from services.wx_usnws          import USNationalWeatherService
#from services.wx_accuweather    import ACCUWeather

def cmdLineOptionParser():
    """
        cmdLineOptionParser()
         - PARSES THE COMMAND LINE ARGUMENTS
         - INPUT:  NONE
         - OUPUTS: NONE
    """
    # CREATE OUR USAGE REPSONSE
    usage = ("%prog [options]",__doc__)

    usage = "\n".join(usage)
    
    # CREATE OUR COMMAND LINE PARSER
    cmdparser = optparse.OptionParser(usage)
    
    # MAIN GROUP OPTIONS    
    cmdparser.add_option('-d', '--debug', action='store_true', 
        help="Enable debugging",
        default=False
    )
    
    cmdparser.add_option('-M', '--metric', action='store_true', 
        help="Use Metric Units (not supported for all sites, currently only works for Yahoo! Weather)",
        default=False
    )

    cmdparser.add_option('-H', '--hideprovides', action='store_true',
        help="Hide the Provided by line in the output",
        default=False
    )
    
    cmdparser.add_option('-U', '--url', action='store', type='string',
        help="User input URL if you are bypassing the automatic location grabbing feature",
        default=''
    )
    
    cmdparser.add_option('-T', '--weathertype', action='store', type='string',
        help="Specify the place you want your weather from: yahoo, weatherchannel, wunderground, weatherbug, usnws",
        default="yahoo"
    )

    cmdparser.add_option('-o', '--orientation', action='store', type='string',
        help="Specify the orientation of weather data for Weather Underground-> multiday or US NWS-> multidaysimple: horizontal/vertical",
        default="vertical"
    )

    cmdparser.add_option('-s', '--currentoutputtype', action='store', type='string',
        help="Specify how the Current weather data for the weather sites is displayed: detailed/simple",
        default="detailed"
    )
    
    # LOCATION GROUP OPTIONS
    g1 = optparse.OptionGroup(cmdparser,"Location Options","Options Specific to Location Services")
        
    g1.add_option('-L', '--locserv', action='store', type='string',
        help="Specify the IP to Location grabbing service to use: ipinfodb", # or ipfingerprints",
        default='ipinfodb'
    )
    
    g1.add_option('-Q', '--yql_loc_type', action='store', type='string',
        help="Specify how the YQL gets the WOEID: zip/full",
        default='full'
    )
    
    g1.add_option('-A', '--locgrabber', action='store_true',
        help="Tell the script to use the Location grabbing function",
        default=False
    )
    
    g1.add_option('-B', '--locfeeder', action='store_true',
        help="Tell the script to use the Location you provide with the -C, -S, -O, and -Z options",
        default=False
    )
    
    g1.add_option('-C', '--city', action='store', type='string',
        help="City of user input location",
        default=''
    )
    
    g1.add_option('-S', '--stateprov', action='store', type='string',
        help="State or Province of user input location",
        default=''
    )
    
    g1.add_option('-O', '--country', action='store', type='string',
        help="Country of user input location",
        default=''
    )
    
    g1.add_option('-Z', '--zipcode', action='store', type='string',
        help="Zip code of user input location",
        default=''
    )
    
    # ADD GROUP 1 TO THE OPTION PARSER
    cmdparser.add_option_group(g1)
    
    # YAHOO WEATHER GROUP OPTIONS
    g2 = optparse.OptionGroup(cmdparser,"Yahoo! Weather Options","Options Specific to Yahoo! Weather, use only if -T is set to: yahoo")
    
    g2.add_option('-e', '--yahoofcasttype', action='store', type='string',
        help="Specify the type of forecast to display: current,twoday,fivedaysimple,fivedaydetail",
        default="current"
    )
    # ADD GROUP 2 TO THE OPTION PARSER
    cmdparser.add_option_group(g2)
    
    # WEATHER.COM GROUP OPTIONS
    #g3 = optparse.OptionGroup(cmdparser,"Weather Channel Options","Options Specific to Weather Channel, use only if -T is set to: weatherchannel")
    
    #g3.add_option('-f', '--weatherdotcomfcasttype', action='store', type='string',
    #    help="Specify the type of forecast to display: current,tomorrow,fiveday,tenday",
    #    default="current"
    #)
    # ADD GROUP 3 TO THE OPTION PARSER
    #cmdparser.add_option_group(g3)
    
    # WUNDERGROUND GROUP OPTIONS
    g4 = optparse.OptionGroup(cmdparser,"Weather Underground Options","Options Specific to Weather Underground, use only if -T is set to: wunderground")
    
    g4.add_option('-g', '--wundergroundfcasttype', action='store', type='string',
        help="Specify the type of forecast to display: current,multiday",
        default="current"
    )
    
    g4.add_option('-n', '--wundergroundnumdays', action='store', type='int',
        help="Specify the number of days to grab for the wunderground multi-day forecast (1 to 10)",
        default=5
    )
    
    # ADD GROUP 4 TO THE OPTION PARSER
    cmdparser.add_option_group(g4)
    
    
    # US NATIONAL WEATHER GROUP OPTIONS
    g5 = optparse.OptionGroup(cmdparser,"US National Weather Service Options","Options Specific to US National Weather Service, use only if -T is set to: uwnws")
    
    g5.add_option('-i', '--usnwsfcasttype', action='store', type='string',
        help="Specify the type of forecast to display: current,multidaysimple,multidaydetailed",
        default="current"
    )
    
    # ADD GROUP 5 TO THE OPTION PARSER
    cmdparser.add_option_group(g5)
    
    # ACCUWEATHER GROUP OPTIONS
    #g6 = optparse.OptionGroup(cmdparser,"ACCUWeather Options","Options Specific to ACCUWeather, use only if -T is set to: accuweather")
    
    #g6.add_option('-j', '--accuwxfcasttype', action='store', type='string',
    #    help="Specify the type of forecast to display: current,multiday",
    #    default="current"
    #)
    # ADD GROUP 6 TO THE OPTION PARSER
    #cmdparser.add_option_group(g6)
    
    
    # RETURN THE PARSER
    return cmdparser

def verifyOpts(opts):
    """
        verifyOpts()
         - FUNCTION TO VERIFY THE COMMAND LINE ARGUMENTS FOR VALIDITY
         - INPUT:  opts - COMMAND LINE OPTIONS
         - OUPUTS: rtnval - 0 IF GOOD, 1 IF VALIDITY CHECK FAILED
    """
    # VARIABLE DECLARATIONS
    rtnval1 = 0
    rtnval2 = 0
    rtnval3 = 0
    
    # CHECK TO SEE IF THE SITE TYPE IS IN THE DICTIONARY LIST
    if opts.weathertype not in WEATHERSERVICES:
        print "*** INVALID WEATHER TYPE SPECIFIED ***"
        rtnval1 = 1
    
    # CHECK TO SEE IF THERE IS NO LOCATION INFORMATION SPECIFIED
    if not opts.locgrabber and not opts.locfeeder and opts.url == '':
        print "***          NO LOCATION SERVICE/INPUT OR URL PROVIDED          ***"
        print "*** PLEASE ENABLE EITHER -A, -B (WITH -C, -S, -O, -Z), OR --url ***"
        rtnval2 = 1
    
    # CHECK
    if opts.weathertype == 'wunderground':
        if opts.wundergroundnumdays < 0 or opts.wundergroundnumdays > 10:
            print "*** INVALID NUMBER OF PRINTABLE WUNDERGROUND FORECASTS ***"
            rtnval3 = 1
    
    
    # RETURN TO MAIN
    return (rtnval1 or rtnval2 or rtnval3)

def Main(argv):
    """
        Main()
         - MAIN SCRIPT FUNCTION THAT WILL GET FACEBOOK FEED INFORMATION
         - INPUT:  argv - COMMAND LINE ARGUMENTS
         - OUPUTS: NONE
    """

    # FIGURE OUT COMMAND LINE ARGUMENTS
    cmdparser = cmdLineOptionParser()
    opts, args = cmdparser.parse_args(argv)

    # VALIDATE THE COMMAND LINE OPTIONS
    if verifyOpts(opts):
        print "*** SCRIPT EXITING ***"
        sys.exit(1)
    
    # FIGURE OUT WHAT WEATHER WE WANT TO GET
    if opts.weathertype == "yahoo":
        myweather = YahooWeather()
    elif opts.weathertype == "weatherchannel":
        print "not yet supported"
        sys.exit(1)
        #myweather = WeatherChannel()
    elif opts.weathertype == "wunderground":
        myweather = WeatherUnderground()
    elif opts.weathertype == "weatherbug":
        print "not yet supported"
        sys.exit(1)
    elif opts.weathertype == "usnws":
        myweather = USNationalWeatherService()
    elif opts.weathertype == "accuweather":
        print "not yet supported"
        sys.exit(1)
        #myweather = ACCUWeather()

    # DO WORK - ALL forecasts.Forecast BASES CLASSES NEED TO
    # HAVE ALL OF THESE FUNCTIONS
    myweather.setLocationData(opts)
    myweather.setURL(opts)
    myweather.getData(opts)
    myweather.parseData(opts)
    myweather.printForecasts(opts)
    
if __name__ == "__main__":
    Main(sys.argv[1:])

