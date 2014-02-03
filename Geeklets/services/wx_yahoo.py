""" YahooWeather
 ROBERT WOLTERMAN (xtacocorex) - 2012

 GRABS THE WEATHER FROM THE YAHOO WEATHER SITE
 
 THIS CLASS INHERITS FROM forecasts.Forecasts 
"""

# MODULE IMPORTS
from globals          import *
from utilityfunctions import *
import forecasts

# CHANGELOG
# 21 APRIL 2012
#  - EXTRACTION FROM THE MAIN SCRIPT AND PUT INTO THE SERVICES MODULE
#  - KNOWN ISSUES: SETTING THE 5 DAY SIMPLE AND DETAILED FORECASTS DOES
#                  NOT WORK DUE TO A CHANGE IN THE HTML SOURCE

class YahooWeather(forecasts.Forecasts):
    def __init__(self):
        self.baseimgurl = "http://l.yimg.com/a/i/us/we/52/%s.gif"
        # INITIALIZE THE INHERITED CLASS
        forecasts.Forecasts.__init__(self)
                
    def setURL(self,opts):

        if opts.yahoofcasttype == 'current' or opts.yahoofcasttype == 'twoday':
            # DETERMINE IF WE ARE USING A HARDCODED URL
            if opts.url != '':
                # YOU ARE ON YOUR OWN FOR PROVIDING UNITS WITH THE HARD CODED URL
                yqlquery = 'select * from xml where url="%s"' % opts.url
            else:
                if opts.metric:
                    u = "c"
                else:
                    u = "f"
                yqlquery = 'select * from xml where url="http://weather.yahooapis.com/forecastrss?w=%s&u=%s"' % (self.location.woeid,u)
            self.url = YQLBASEURL + "?q=" + myencode(yqlquery) + "&format=" + YQLFORMAT1
            if opts.debug:
                print "\n*** current and twoday url creation"
                print yqlquery
                print self.url
                print DEBUGSPACER
        elif opts.yahoofcasttype == 'fivedaysimple' or opts.yahoofcasttype == 'fivedaydetail':
            # DETERMINE IF WE ARE USING A HARDCODED URL
            if opts.url != '':
                # YOU ARE ON YOUR OWN FOR PROVIDING UNITS WITH THE HARD CODED URL
                yqlquery = 'select * from html where url="%s"' % opts.url
            else:
                if opts.metric:
                    u = "c"
                else:
                    u = "f"
                mytuple = (self.location.country.replace(" ","-"),self.location.stprov.replace(" ","-"),self.location.city.replace(" ","-"),self.location.woeid,u)
                yqlquery = 'select * from html where url="http://weather.yahoo.com/%s/%s/%s-%s/?unit=%s"' % mytuple
            # FIGURE OUT WHAT WE WANT TO GET FROM THE YQL
            if opts.yahoofcasttype == 'fivedaysimple':
                ender = ' and xpath=\'//div[@id="yw-fivedayforecast"]\''
            elif opts.yahoofcasttype == 'fivedaydetail':
                ender = ' and xpath=\'//div[@id="yw-detailedforecast"]\''
            # CREATE THE URL
            self.url = YQLBASEURL + "?q=" + myencode(yqlquery+ender) + "&format=" + YQLFORMAT1
            if opts.debug:
                print "\n*** fiveday url creation"
                print yqlquery
                print self.url
                print DEBUGSPACER
    
    def parseData(self,opts):
        # CLEAR OUT THE FORECAST LIST
        self.forecasts = []
    
        # DETERMINE IF WHAT WE ARE PARSING
        if   opts.yahoofcasttype == 'current':
            # GET THE UNITS
            self.units          = self.jsondata['query']['results']['rss']['channel']['units']
            # GET THE CURRENT CONDITION
            tmpfcast = forecasts.FCDay()
            tmpfcast.condition  = self.jsondata['query']['results']['rss']['channel']['item']['condition']['text']
            tmpfcast.curtemp    = self.jsondata['query']['results']['rss']['channel']['item']['condition']['temp']
            tmpfcast.date       = self.jsondata['query']['results']['rss']['channel']['item']['condition']['date']
            tmpfcast.code       = self.jsondata['query']['results']['rss']['channel']['item']['condition']['code']
            tmpfcast.imageurl   = self.baseimgurl % tmpfcast.code
            fext = tmpfcast.imageurl[-4:]
            getImage(tmpfcast.imageurl,"yahoo_current_wx"+fext,IMAGESAVELOCATION)
            # HIGH, LOW, AND DAY ARE PROVIDED IN THE FIRST FORECAST ITEM
            tmpfcast.high       = self.jsondata['query']['results']['rss']['channel']['item']['forecast'][0]['high']
            tmpfcast.low        = self.jsondata['query']['results']['rss']['channel']['item']['forecast'][0]['low']
            tmpfcast.day        = self.jsondata['query']['results']['rss']['channel']['item']['forecast'][0]['day']
            # OTHER INFORMATION CONTAINED FOR THE CURRENT CONDITION
            tmpfcast.humidity   = self.jsondata['query']['results']['rss']['channel']['atmosphere']['humidity']
            tmpfcast.pressure   = self.jsondata['query']['results']['rss']['channel']['atmosphere']['pressure']
            tmpfcast.presrise   = self.jsondata['query']['results']['rss']['channel']['atmosphere']['rising']
            tmpfcast.visibility = self.jsondata['query']['results']['rss']['channel']['atmosphere']['visibility']
            tmpfcast.sunrise    = self.jsondata['query']['results']['rss']['channel']['astronomy']['sunrise']
            tmpfcast.sunset     = self.jsondata['query']['results']['rss']['channel']['astronomy']['sunset']
            # APPEND THIS TO THE FORECAST LIST
            self.forecasts.append(tmpfcast)
            # DEBUG
            if opts.debug:
                print tmpfcast
            
        elif opts.yahoofcasttype == 'twoday':
            # GET THE UNITS
            self.units          = self.jsondata['query']['results']['rss']['channel']['units']
            # GET THE NUMBER OF ITEMS IN THE FORECAST
            self.numfcasts      = len(self.jsondata['query']['results']['rss']['channel']['item']['forecast'])
            # LOOP THROUGH AND GET THE FORECAST DATA
            for i in xrange(self.numfcasts):
                # GET THE CURRENT CONDITION
                tmpfcast = forecasts.FCDay()
                tmpfcast.condition  = self.jsondata['query']['results']['rss']['channel']['item']['forecast'][i]['text']
                tmpfcast.date       = self.jsondata['query']['results']['rss']['channel']['item']['forecast'][i]['date']
                tmpfcast.day        = self.jsondata['query']['results']['rss']['channel']['item']['forecast'][i]['day']
                tmpfcast.code       = self.jsondata['query']['results']['rss']['channel']['item']['forecast'][i]['code']
                tmpfcast.imageurl   = self.baseimgurl % tmpfcast.code
                fext = tmpfcast.imageurl[-4:]
                myfname = "yahoo_fcast_day%d%s" % (i+1,fext)
                getImage(tmpfcast.imageurl,myfname,IMAGESAVELOCATION)
                # HIGH AND LOW ARE PROVIDED IN THE FIRST FORECAST ITEM
                tmpfcast.high       = self.jsondata['query']['results']['rss']['channel']['item']['forecast'][i]['high']
                tmpfcast.low        = self.jsondata['query']['results']['rss']['channel']['item']['forecast'][i]['low']
                # APPEND THIS TO THE FORECAST LIST
                self.forecasts.append(tmpfcast)
                # DEBUG
                if opts.debug:
                    print tmpfcast
                    
        elif opts.yahoofcasttype == 'fivedaysimple':
            # GET NUMBER OF FORECASTS
            self.numfcasts      = len(self.jsondata['query']['results']['div']['table']['tr'][0]['th']) - 1
            # LOOP THROUGH AND GET THE FORECAST DATA
            for i in xrange(self.numfcasts):
                # GET THE CURRENT CONDITION
                tmpfcast = forecasts.FCDay()
                tmpfcast.day        = self.jsondata['query']['results']['div']['table']['tr'][0]['th'][i]['p']
                tmpfcast.condition  = self.jsondata['query']['results']['div']['table']['tr'][1]['td'][i]['p']
                t1 = removeNonAscii(self.jsondata['query']['results']['div']['table']['tr'][2]['td'][i]['p'])
                t1 = t1.split(": ")[1]
                tmpfcast.high       = t1
                t2 = removeNonAscii(self.jsondata['query']['results']['div']['table']['tr'][2]['td'][i]['div']['p'])
                t2 = t2.split(": ")[1]
                tmpfcast.low        = t2
                # APPEND THIS TO THE FORECAST LIST
                self.forecasts.append(tmpfcast)
                # DEBUG
                if opts.debug:
                    print tmpfcast
            
        elif opts.yahoofcasttype == 'fivedaydetail':
            # GET NUMBER OF FORECASTS
            self.numfcasts      = len(self.jsondata['query']['results']['div']['ul']['li'])
            # LOOP THROUGH AND GET THE FORECAST DATA
            for i in xrange(self.numfcasts):
                # GET THE CURRENT CONDITION
                tmpfcast = forecasts.FCDay()
                tmpfcast.condition  = self.jsondata['query']['results']['div']['ul']['li'][i]['p']
                tmpfcast.day        = self.jsondata['query']['results']['div']['ul']['li'][i]['strong'].split(":")[0]
                # APPEND THIS TO THE FORECAST LIST
                self.forecasts.append(tmpfcast)
                # DEBUG
                if opts.debug:
                    print tmpfcast
        
    def printForecasts(self, opts):
        # DETERMINE IF WHAT WE ARE PRINTING
        if   opts.yahoofcasttype == 'current':
            if opts.currentoutputtype == 'detailed':
                print "%s %s%s" % (self.forecasts[0].condition,self.forecasts[0].curtemp,self.units['temperature'])
            if opts.currentoutputtype == 'detailed':
                print "H: %s%s L: %s%s" % (self.forecasts[0].high,self.units['temperature'],self.forecasts[0].low,self.units['temperature'])
                print "Humidity:   %s%%" % (self.forecasts[0].humidity)
                print "Pressure:   %s%s" % (self.forecasts[0].pressure,self.units['pressure'])
                print "Visibility: %s%s" % (self.forecasts[0].visibility,self.units['distance'])
                
            if not opts.hideprovides:
                print "Yahoo! Weather provided by Weather.com"
        elif opts.yahoofcasttype == 'twoday':
            mystr = "%s %s\n%s\nHigh: %s%s\nLow:  %s%s"
            for fcast in self.forecasts:
                print mystr % (fcast.day,fcast.date,fcast.condition,fcast.high,self.units['temperature'],fcast.low,self.units['temperature'])
            if not opts.hideprovides:
                print "Yahoo! Weather provided by Weather.com"
        elif opts.yahoofcasttype == 'fivedaysimple':
            mystr = "%s: %s\nHigh: %3s%1s Low:  %3s%1s"
            if opts.metric:
                tempunit = "C"
            else:
                tempunit = "F"
            for fcast in self.forecasts:
                print mystr % (fcast.day,fcast.condition,fcast.high,tempunit,fcast.low,tempunit)
            if not opts.hideprovides:
                print "Yahoo! Weather provided by Weather.com"
        elif opts.yahoofcasttype == 'fivedaydetail':
            mystr = "%s:\n %s"
            for fcast in self.forecasts:
                print mystr % (fcast.day,fcast.condition)
            if not opts.hideprovides:
                print "Yahoo! Weather provided by Weather.com"
