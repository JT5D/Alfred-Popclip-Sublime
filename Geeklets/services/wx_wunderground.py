""" WeatherUnderground
 ROBERT WOLTERMAN (xtacocorex) - 2012

 GRABS THE WEATHER FROM THE WEATHER UNDERGROUND SITE
 
 THIS CLASS INHERITS FROM forecasts.Forecasts 
"""

# MODULE IMPORTS
from globals          import *
from utilityfunctions import *
import forecasts

# CHANGELOG
# 21 APRIL 2012
#  - EXTRACTION FROM THE MAIN SCRIPT AND PUT INTO THE SERVICES MODULE

class WeatherUnderground(forecasts.Forecasts):
    def __init__(self):
        # INITIALIZE THE INHERITED CLASS
        forecasts.Forecasts.__init__(self)

    def setURL(self,opts):
        # FIGURE OUT OUR URL FOR WORK
        # DETERMINE IF WE ARE USING A HARDCODED URL
        if opts.url != '':
            # YOU ARE ON YOUR OWN FOR PROVIDING UNITS WITH THE HARD CODED URL
            yqlquery = 'select * from html where url="%s"' % opts.url
        else:
            #    if opts.metric:
            #        u = "c"
            #    else:
            #        u = "f"
            if self.location.country == "united states":
                wquery = "%s+%s" % (self.location.city.replace(" ","+"),self.location.stprov.replace(" ","+"))
            else:
                wquery = "%s+%s+%s" % (self.location.city.replace(" ","+"),self.location.stprov.replace(" ","+"),self.location.country.replace(" ","+"))
            yqlquery = 'select * from html where url="http://www.wunderground.com/cgi-bin/findweather/hdfForecast?query=%s"' % wquery
        # FIGURE OUT WHAT WE WANT TO GET FROM THE YQL
        if   opts.wundergroundfcasttype == 'current':
            # THE TOOL IN OPERA THAT ALLOWS YOU TO EXPLORE HTML SOURCE IS AWESOME
            ender = ' and xpath=\'//div[@id="curIcon"]|//div[@id="curCond"]|//div[@id="nowTemp"]|//div[@id="nowSuns"]|//div[@id="curData1"]|//div[@id="curData2"]\''
        elif opts.wundergroundfcasttype == 'multiday':
            ender = ' and xpath=\'//div[@class="fctScrollContain"]\''
        self.url = YQLBASEURL + "?q=" + myencode(yqlquery+ender) + "&format=" + YQLFORMAT1
        if opts.debug:
            print "\n*** wunderground url creation"
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
        if   opts.wundergroundfcasttype == 'current':
            # GET THE UNITS
            self.units['temperature'] = removeNonAscii(self.jsondata['query']['results']['div'][2]['div'][1]['span']['span']['content']).strip() #.replace('\u00a0\u00b0','').strip() #GOOD
            self.units['sriseperiod'] = self.jsondata['query']['results']['div'][3]['div'][1]['p']
            self.units['ssetperiod']  = self.jsondata['query']['results']['div'][3]['div'][2]['p']
            self.units['pressure']    = self.jsondata['query']['results']['div'][4]['div'][0]['div'][2]['span']['content'].replace('\u00a0','').strip() #GOOD
            self.units['distance']    = self.jsondata['query']['results']['div'][4]['div'][0]['div'][5]['span']['content'].replace('\u00a0','').strip() #GOOD
            try:
                self.units['speed']   = self.jsondata['query']['results']['div'][5]['div'][1]['div'][2]['span']['span']['content'].replace('\u00a0','').strip() #GOOD
            except:
                self.units['speed']   = self.jsondata['query']['results']['div'][5]['div'][1]['div'][4]['span']['span']['content'].replace('\u00a0','').strip() #GOOD
            else:
                self.units['speed']   = "" # IF THERE IS NO WIND, THERE IS NO NEED FOR SPEED
            # GET THE CURRENT CONDITION
            tmpfcast = forecasts.FCDay()
            tmpfcast.imageurl   = self.jsondata['query']['results']['div'][0]['a']['img']['src'] #GOOD
            fext = tmpfcast.imageurl[-4:]
            getImage(tmpfcast.imageurl,"wunderground_current_wx"+fext,IMAGESAVELOCATION)
            tmpfcast.condition  = self.jsondata['query']['results']['div'][1]['p'] # GOOD
            tmpfcast.curtemp    = self.jsondata['query']['results']['div'][2]['div'][1]['span']['value'] #GOOD
            tmpfcast.tempfeel   = self.jsondata['query']['results']['div'][2]['div'][2]['p']['span']['span']['content'] #GOOD
            tmpfcast.sunrise    = self.jsondata['query']['results']['div'][3]['div'][1]['span']['content'] #GOOD
            tmpfcast.sunset     = self.jsondata['query']['results']['div'][3]['div'][2]['span']['content'] #GOOD
            tmpfcast.pressure   = self.jsondata['query']['results']['div'][4]['div'][0]['div'][2]['span']['value'] #GOOD
            tmpfcast.visibility = self.jsondata['query']['results']['div'][4]['div'][0]['div'][5]['span']['span']['content'] #GOOD
            tmpfcast.humidity   = self.jsondata['query']['results']['div'][4]['div'][1]['div'][2]['span']['value'] #GOOD
            tmpfcast.dewpoint   = self.jsondata['query']['results']['div'][5]['div'][0]['div'][5]['span']['span']['span']['content'] #GOOD
            try:
                tmpfcast.winddir    = self.jsondata['query']['results']['div'][5]['div'][1]['div'][2]['p']['span']['content'] #GOOD
            except:
                tmpfcast.winddir    = ""  # IF THERE IS NO WIND
            try:
                tmpfcast.windspeed  = self.jsondata['query']['results']['div'][5]['div'][1]['div'][2]['span']['span']['span']['content'] #GOOD
            except:
                tmpfcast.windspeed  = self.jsondata['query']['results']['div'][5]['div'][1]['div'][2]['p']
            else:
                tmpfcast.windspeed  = ""
            try:
                tmpfcast.windgust   = self.jsondata['query']['results']['div'][5]['div'][1]['div'][4]['span']['span']['span']['content'] #GOOD
            except:
                tmpfcast.windgust   = "0"   # THERE IS NO WINDGUST
            # APPEND THIS TO THE FORECAST LIST
            self.forecasts.append(tmpfcast)
            # DEBUG
            if opts.debug:
                print tmpfcast
        elif opts.wundergroundfcasttype == 'multiday':
            # GET THE LENGTH OF THE DATA INSIDE THE DICTIONARY
            # THIS SHOULD ALWAYS RETURN 12 AND WE'RE GOING TO SKIP OVER
            # 4 AND 5 (STARTING FROM 0)
            lendict = len(self.jsondata['query']['results']['div']['div'])
            # LOOP THROUGH THE JSON DATA AND GET THE FORECAST INFORMATION
            day = 1
            for i in xrange(lendict):
                tmpfcast = forecasts.FCDay()
                # WE CAN ONLY GET DATE, CONDITION, HIGH, LOW, % PRECIPITATION, AND IMAGE URL
                # SKIP OVER INDEX 4 AND 5            
                if "fctDay" in self.jsondata['query']['results']['div']['div'][i]['class']:
                    # GET THE DATE
                    tmpfcast.date       = self.jsondata['query']['results']['div']['div'][i]['div'][0]['p']
                    tmpfcast.imageurl   = self.jsondata['query']['results']['div']['div'][i]['div'][1]['div'][0]['a']['img']['src']
                    fext = tmpfcast.imageurl[-4:]
                    myfname = "wunderground_fcast_day%d%s" % (day,fext)
                    getImage(tmpfcast.imageurl,myfname,IMAGESAVELOCATION)
                    tmpfcast.high       = self.jsondata['query']['results']['div']['div'][i]['div'][1]['div'][1]['span']['content']
                    tmp = self.jsondata['query']['results']['div']['div'][i]['div'][1]['div'][1]['p'].split(" ")
                    tmpfcast.low        = tmp[1]
                    self.units['temperature'] = removeNonAscii(tmp[2]).strip()   #.replace("\xb0","").strip() #.replace('\u00a0\u00b0','').strip() #GOOD
                    tmpfcast.condition  = self.jsondata['query']['results']['div']['div'][i]['div'][1]['div'][2]['p']
                    tmpfcast.pcntprecip = self.jsondata['query']['results']['div']['div'][i]['div'][1]['div'][3]['div'][1]['p']
                    # APPEND THIS TO THE FORECAST LIST
                    self.forecasts.append(tmpfcast)
                    # INCREMENT DAY
                    day += 1
                    # DEBUG
                    if opts.debug:
                        print tmpfcast
            # SET THE NUMBER OF FORECASTS
            self.numfcasts = day

    def printForecasts(self, opts):
        # DETERMINE IF WHAT WE ARE PRINTING
        if   opts.wundergroundfcasttype == 'current':
            if opts.currentoutputtype == 'detailed':
                print "Condition:   %s" % self.forecasts[0].condition
                u = self.units['temperature']
                mtuple = (self.forecasts[0].curtemp,u,self.forecasts[0].tempfeel,u,self.forecasts[0].dewpoint,u)
                print "Temperature: %3s%s\nFeels Like:  %3s%s\nDew Point:   %3s%s" % mtuple
                print "Humidity:    %3s%%" % (self.forecasts[0].humidity)
                print "Pressure:    %s %s" % (self.forecasts[0].pressure,self.units['pressure'])
                u = self.units['speed']
                if self.forecasts[0].winddir != "":
                    print "Wind: %s%s - %s\nGust: %s%s" % (self.forecasts[0].windspeed,u,self.forecasts[0].winddir,self.forecasts[0].windgust,u)
                else:
                    print "Wind: %s\nGust: %s%s" % (self.forecasts[0].windspeed,self.forecasts[0].windgust,u)
                print "Visibility:  %s %s" % (self.forecasts[0].visibility,self.units['distance'])
                print "---------------"
                print "Sunrise:     %s %s" % (self.forecasts[0].sunrise,self.units['sriseperiod'])
                print "Sunset:      %s %s" % (self.forecasts[0].sunset,self.units['ssetperiod'])
            elif opts.currentoutputtype == 'simple':
                print "%s | %3s%s" % (self.forecasts[0].condition,self.forecasts[0].curtemp,self.units['temperature'])
            if not opts.hideprovides:
                print "wunderground.com"
        elif opts.wundergroundfcasttype == 'multiday':
            # FIGURE OUT HOW USER WANTS DATA DISPLAYED
            if opts.orientation == 'vertical':
                # LOOP THROUGH THE NUMBER THE USER SPECIFIED
                # THE CHECK FOR THIS VALUE WILL HAVE BEEN DONE WHEN THE PROGRAM STARTS
                mystr1 = "%s\n%s\nH: %3s%s L: %3s%s\nPrecipitation: %s\n"
                mystr2 = "%s\n%s\nH: %3s%s L: %3s%s\nPrecipitation: %s"
                for i in xrange(opts.wundergroundnumdays):
                    u = self.units['temperature']
                    mytuple = (self.forecasts[i].date,self.forecasts[i].condition,self.forecasts[i].high,u,self.forecasts[i].low,u,self.forecasts[i].pcntprecip)
                    if i != opts.wundergroundnumdays-1:
                        print mystr1 % mytuple
                    else:
                        print mystr2 % mytuple
            elif opts.orientation == 'horizontal':
                mystr1 = "%16s"
                mystr2 = "High: %3s%s"
                mystr3 = "Low:  %3s%s"
                mystr4 = "Chc Precip: %s"
                datelist = []
                highlist = []
                lowlist  = []
                condlist = []
                preclist = []
                for i in xrange(opts.wundergroundnumdays):
                    tmp = mystr1 % self.forecasts[i].date.ljust(16)
                    datelist.append(tmp)
                    condlist.append(self.forecasts[i].condition)
                    tmp = mystr2 % (self.forecasts[i].low,self.units['temperature'])
                    lowlist.append(tmp)
                    tmp = mystr3 % (self.forecasts[i].high,self.units['temperature'])
                    highlist.append(tmp)
                    tmp = mystr4 % self.forecasts[i].pcntprecip
                    preclist.append(tmp)
                # CREATE OUR MATRIX
                matrix = [datelist,condlist,highlist,lowlist,preclist]
                # PRINT THE TABLE
                printTable(matrix,(5,opts.wundergroundnumdays),'left')
            if not opts.hideprovides:
                print "wunderground.com"
