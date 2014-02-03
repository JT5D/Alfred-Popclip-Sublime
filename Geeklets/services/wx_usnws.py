""" USNationalWeatherService
 ROBERT WOLTERMAN (xtacocorex) - 2012

 GRABS THE WEATHER FROM THE US NATIONAL WEATHER SERVICE SITE
 
 THIS CLASS INHERITS FROM forecasts.Forecasts 
"""

# MODULE IMPORTS
from globals          import *
from utilityfunctions import *
import forecasts

# CHANGELOG
# 21 APRIL 2012
#  - EXTRACTION FROM THE MAIN SCRIPT AND PUT INTO THE SERVICES MODULE

class USNationalWeatherService(forecasts.Forecasts):
    def __init__(self):
        self.baseimgurl = "http://forecast.weather.gov"
        self.havewindchill = False
        # INITIALIZE THE INHERITED CLASS
        forecasts.Forecasts.__init__(self)

    def setURL(self,opts):
        # FIGURE OUT OUR URL FOR WORK
        # DETERMINE IF WE ARE USING A HARDCODED URL
        if opts.url != '':
            # YOU ARE ON YOUR OWN FOR PROVIDING UNITS WITH THE HARD CODED URL
            yqlquery = 'select * from html where url="%s"' % opts.url
        else:
            if self.location.country != "united states":
                print "*** US NATIONAL WEATHER SERVICE IS ONLY FOR RESIDENTS OF THE UNITED STATES ***"
                sys.exit(-1)
            else:
                mytuple = (self.location.city.title().replace(" ","+"),USSTATEMAP[self.location.stprov.title()],self.location.lat,self.location.lon)
            yqlquery = 'select * from html where url="http://forecast.weather.gov/MapClick.php?CityName=%s&state=%s&textField1=%s&textField2=%s"' % mytuple
        # FIGURE OUT WHAT WE WANT TO GET FROM THE YQL
        if   opts.usnwsfcasttype == 'current':
            # THE TOOL IN OPERA THAT ALLOWS YOU TO EXPLORE HTML SOURCE IS AWESOME
            ender = ' and xpath=\'//div[@id="container"]/table[4]/tr[2]/td/table[2]/tr/td[2]/table/tr[2]/td/table/tr\''
        elif opts.usnwsfcasttype == 'multidaysimple':
            ender = ' and xpath=\'//div[@id="container"]/table[4]/tr[2]/td/table/tr\''
        elif opts.usnwsfcasttype == 'multidaydetailed':
            ender = ' and xpath=\'//div[@id="container"]/table[4]/tr[2]/td/table[2]/tr/td\''
        self.url = YQLBASEURL + "?q=" + myencode(yqlquery+ender) + "&format=" + YQLFORMAT1
        if opts.debug:
            print "\n*** us nws url creation"
            print yqlquery
            print self.url
            print DEBUGSPACER
    
    def parseData(self,opts):
        # CLEAR OUT THE FORECAST LIST
        self.forecasts = []
        # CREATE OUR UNITS DICTIONARY
        self.units = {'temperature' : '',
                      'pressure'    : '',
                      'distance'    : '',
                      'speed'       : '',
                      'sriseperiod' : '',
                      'ssetperiod'  : ''
                      }
        # DETERMINE WHAT WE ARE PARSING
        if   opts.usnwsfcasttype == 'current':
            # THE INTERESTING THING ABOUT THE CURRENT FORECAST ON THE NWS SITE
            # IS THAT IT PROVIDES METRIC NEXT TO THE FAHRENHEIT DATA
            tmpfcast = forecasts.FCDay()
            # LETS GET THE TEMPERATURE
            tempdata = removeNonAscii(self.jsondata['query']['results']['tr']['td'][0]['p']['content'])
            tempdata = tempdata.replace("\n                              ","-")
            tempdata = tempdata.split("--")
            tmpfcast.condition  = tempdata[0]
            tempdata = tempdata[1].split("-")
            if opts.metric:
                tmp                       = tempdata[1].split(" ")
                tmpfcast.curtemp          = tmp[0].split("(")[1]
                self.units['temperature'] = tmp[1].split(")")[0]
            else:
                tmp                       = tempdata[0].split(" ")
                tmpfcast.curtemp          = tmp[0]
                self.units['temperature'] = tmp[1]
            # HUMIDITY
            tmpfcast.humidity = self.jsondata['query']['results']['tr']['td'][1]['table']['tr'][0]['td'][1]['p']
            # WIND AND GUST
            winddata = self.jsondata['query']['results']['tr']['td'][1]['table']['tr'][1]['td'][1]['p'].split(" ")
            if len(winddata) == 3:
                tmpfcast.winddir    = winddata[0]
                tmpfcast.windspeed  = winddata[1]
                tmpfcast.windgust   = "0"
                self.units['speed'] = winddata[2]
            else:
                tmpfcast.windgust   = winddata[3]
                self.units['speed'] = winddata[4]
            # PRESSURE
            presdata = self.jsondata['query']['results']['tr']['td'][1]['table']['tr'][2]['td'][1]['p'].split(" ")
            if opts.metric:
                tmpfcast.pressure   = presdata[1].split("(")[1]
                self.units['pressure'] = presdata[2].split(")")[0]
            else:
                tmpfcast.pressure   = presdata[0].split('"')[0]
                self.units['pressure'] = "in"
            # DEW POINT
            dewdata = removeNonAscii(self.jsondata['query']['results']['tr']['td'][1]['table']['tr'][3]['td'][1]['p']).split("-")
            if opts.metric:
                tmp                       = dewdata[1].split(" ")
                tmpfcast.dewpoint          = tmp[0].split("(")[1]
            else:
                tmp                       = dewdata[0].split(" ")
                tmpfcast.dewpoint          = tmp[0]
            
            # HAVE TO WORK AROUND THE WIND CHILL NOT SHOWING UP ALL THE TIME
            if self.jsondata['query']['results']['tr']['td'][1]['table']['tr'][4]['td'][0]['strong'] == "Wind Chill":
                feeldata = removeNonAscii(self.jsondata['query']['results']['tr']['td'][1]['table']['tr'][4]['td'][1]['p']).split("-")
                self.havewindchill = True
                if opts.metric:
                    tmp                       = feeldata[1].split(" ")
                    tmpfcast.tempfeel          = tmp[0].split("(")[1]
                else:
                    tmp                       = feeldata[0].split(" ")
                    tmpfcast.tempfeel          = tmp[0]
                # WIND CHILL - FOR SOME REASON THIS DATA ISN'T HERE ALL THE TIME
                tmpfcast.tempfeel   = "--"
                # VISIBILITY
                visidata = self.jsondata['query']['results']['tr']['td'][1]['table']['tr'][5]['td'][1]['p'].split(" ")
                tmpfcast.visibility = visidata[0]
                self.units['distance'] = visidata[1]
            else:
                # VISIBILITY
                visidata = self.jsondata['query']['results']['tr']['td'][1]['table']['tr'][4]['td'][1]['p'].split(" ")
                tmpfcast.visibility = visidata[0]
                self.units['distance'] = visidata[1]
            # APPEND THIS TO THE FORECAST LIST
            self.forecasts.append(tmpfcast)
            # DEBUG
            if opts.debug:
                print tmpfcast
        elif opts.usnwsfcasttype == 'multidaysimple':
            # GET THE NUMBER OF ITEMS IN THE 'td' LIST, THERE SHOULD BE NINE
            self.numfcasts = len(self.jsondata['query']['results']['tr'][0]['td'])
            # SET OUR VARIABLE TO SEE IF WE ARE IN A NIGHT ITEM
            innight = False
            # LOOP THROUGH THE NUMBER OF FORECASTS AND GET THE DATA
            for i in xrange(self.numfcasts):
                tmpfcast = forecasts.FCDay()
                # WE CAN ONLY GET DATE, CONDITION, HIGH OR LOW, % PRECIPITATION, AND IMAGE URL
                tmpfcast.date       = self.jsondata['query']['results']['tr'][0]['td'][i]['strong']['content'].rstrip()
                # FIGURE OUT IF WE ARE DOING A NIGHT TIME FORECAST OR NOT
                if "Night" in tmpfcast.date or "Afternoon" in tmpfcast.date:
                    tmpfcast.date   = tmpfcast.date.replace("\n                  "," ")
                # WEATHER IMAGE
                imgloc              = self.jsondata['query']['results']['tr'][0]['td'][i]['img']['src']
                tmpfcast.imageurl   = self.baseimgurl + imgloc
                fext = tmpfcast.imageurl[-4:]
                myfname = "usnws_fcast_day%d%s" % (i+1,fext)
                getImage(tmpfcast.imageurl,myfname,IMAGESAVELOCATION)
                # TEMPERATURE
                temperature          = self.jsondata['query']['results']['tr'][0]['td'][i]['p']['font']['content']
                # BASE TEMPERATURES ON IF WE ARE LOOKING FOR A HIGH OR A LOW IN THE TABLE DATA
                if "Lo" == self.jsondata['query']['results']['tr'][0]['td'][i]['p']['content'].replace(" \n                  ","")[-2:]:
                    tmpfcast.low     = temperature.split(" ")[0]
                    tmpfcast.high    = "--"
                else:
                    tmpfcast.high    = temperature.split(" ")[0]
                    tmpfcast.low     = "--"
                self.units['temperature'] = temperature[-1:]
                # CONDITION
                tmp                  = self.jsondata['query']['results']['tr'][0]['td'][i]['p']['content'].replace("\n                  "," ").rstrip()
                tmp                  = tmp.split(" ")
                condition = ""
                for i in xrange(len(tmp)-1):
                    condition += tmp[i] + " "
                tmpfcast.condition   = condition.rstrip()
                # CHANCE OF PRECIPITATION
                imgalttest = self.jsondata['query']['results']['tr'][0]['td'][i]['img']['alt']
                if "Change for Measureable Precipitation" in imgalttest:
                    tmp = imgalttest.split(" ")
                    tmpfcast.pcntprecip = tmp[-1:]
                else:
                    tmpfcast.pcntprecip = "0%"
                # APPEND THIS TO THE FORECAST LIST
                self.forecasts.append(tmpfcast)
                # DEBUG
                if opts.debug:
                    print tmpfcast
        elif opts.usnwsfcasttype == 'multidaydetailed':
            # GET THE DATA FOR THE DETAILED FORECAST, IT IS ALL CONTAINED IN ONE LINE
            fcastdata = self.jsondata['query']['results']['td'][0]['p'][1]['content'].replace("\n                \n                ","")
            fcastdata = fcastdata.split("\n                 ")
            # GET THE DAY NAMES
            daynames  = []
            daynames.append(self.jsondata['query']['results']['td'][0]['strong'])
            daynames += self.jsondata['query']['results']['td'][0]['p'][1]['strong']
            # SET THE NUMBER OF FORECASTS
            self.numfcasts = len(fcastdata)
            # LOOP THROUGH THE LISTS AND CREATE OUR FORECAST DAY OBJECTS
            for i in xrange(self.numfcasts):
                tmpfcast = forecasts.FCDay()
                # SET THE DATE
                tmpfcast.date      = daynames[i]
                tmpfcast.condition = fcastdata[i]
                # APPEND THIS TO THE FORECAST LIST
                self.forecasts.append(tmpfcast)
                # DEBUG
                if opts.debug:
                    print tmpfcast

    def printForecasts(self, opts):
        # DETERMINE IF WHAT WE ARE PRINTING
        if   opts.usnwsfcasttype == 'current':
            if opts.currentoutputtype == 'detailed':
                print "Condition:   %s" % self.forecasts[0].condition
                u = self.units['temperature']
                if self.havewindchill:
                    mtuple = (self.forecasts[0].curtemp,u,self.forecasts[0].tempfeel,u,self.forecasts[0].dewpoint,u)
                    print "Temperature: %3s%s\nFeels Like:  %3s%s\nDew Point:   %3s%s" % mtuple
                else:
                    mtuple = (self.forecasts[0].curtemp,u,self.forecasts[0].dewpoint,u)
                    print "Temperature: %3s%s\nDew Point:   %3s%s" % mtuple
                print "Humidity:    %3s" % (self.forecasts[0].humidity)
                print "Pressure:    %s %s" % (self.forecasts[0].pressure,self.units['pressure'])
                u = self.units['speed']
                if self.forecasts[0].winddir != "":
                    print "Wind: %s%s - %s\nGust: %s%s" % (self.forecasts[0].windspeed,u,self.forecasts[0].winddir,self.forecasts[0].windgust,u)
                else:
                    print "Wind: %s\nGust: %s%s" % (self.forecasts[0].windspeed,self.forecasts[0].windgust,u)
                print "Visibility:  %s %s" % (self.forecasts[0].visibility,self.units['distance'])
            elif opts.currentoutputtype == 'simple':
                print "%s | %3s%s" % (self.forecasts[0].condition,self.forecasts[0].curtemp,self.units['temperature'])
            if not opts.hideprovides:
                print "forecast.weather.gov"
        elif opts.usnwsfcasttype == 'multidaysimple':
            # FIGURE OUT THE ORIENTATION OF PRINTING DATA
            if   opts.orientation == 'vertical':
                mystr = "%s\n%s\n%s: %3s%s\nPrecipitation: %s\n"
                for fcast in self.forecasts:
                    if fcast.high == '--':
                        mytuple = (fcast.date,fcast.condition,"L",fcast.low,self.units['temperature'],fcast.pcntprecip)
                    elif fcast.low == '--':
                        mytuple = (fcast.date,fcast.condition,"H",fcast.high,self.units['temperature'],fcast.pcntprecip)
                    print mystr % mytuple
            elif opts.orientation == 'horizontal':
                mystr1 = "%16s"
                mystr2 = "High: %3s%s"
                mystr3 = "Low:  %3s%s"
                mystr4 = "Chc Precip: %s"
                datelist = []
                templist = []
                condlist = []
                preclist = []
                for fcast in self.forecasts:
                    tmp = mystr1 % fcast.date.ljust(16)
                    datelist.append(tmp)
                    condlist.append(fcast.condition)
                    if fcast.high == '--':
                        tmp = mystr2 % (fcast.low,self.units['temperature'])
                    elif fcast.low == '--':
                        tmp = mystr3 % (fcast.high,self.units['temperature'])
                    templist.append(tmp)
                    tmp = mystr4 % fcast.pcntprecip
                    preclist.append(tmp)
                # CREATE OUR MATRIX
                matrix = [datelist,condlist,templist,preclist]
                # PRINT THE TABLE
                printTable(matrix,(4,9),'left')
                if not opts.hideprovides:
                    print "forecast.weather.gov"
        elif opts.usnwsfcasttype == 'multidaydetailed':
            # LOOP THROUGH THE FORECASTS AND PRINT THE DATA
            mystr = "%s\n%s\n"
            for fcast in self.forecasts:
                print mystr % (fcast.date,fcast.condition)
            if not opts.hideprovides:
                print "forecast.weather.gov"

