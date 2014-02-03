""" forecasts
 ROBERT WOLTERMAN (xtacocorex) - 2012

 FORECAST BASE CLASSES - ALL SERVICES SHOULD INHERIT Forecast 
 AND SHOULD STORE ALL FORECAST DAY DATA INTO FCDay
"""

# CHANGELOG
# 21 APRIL 2012
#  - EXTRACTION FROM THE MAIN SCRIPT AND PUT INTO THE SERVICES MODULE

# MODULE IMPORTS
import urllib2, json
import location
from globals import *

class FCDay:
    def __init__(self):
        # NOT ALL WEATHER SITES SUPPORT THESE FIELDS
        self.condition  = "--"
        self.high       = "--"
        self.low        = "--"
        self.curtemp    = "--"
        self.date       = "--"
        self.day        = "--"
        self.code       = "--"
        self.imageurl   = "--"
        self.pcntprecip = "--"
        # OTHER DATA THAT ISN'T PUT IN THE __REPR__
        self.sunrise    = "--"
        self.sunset     = "--"
        self.windspeed  = "--"
        self.windgust   = "--"
        self.winddir    = "--"
        self.tempfeel   = "--"
        self.humidity   = "--"
        self.dewpoint   = "--"
        self.pressure   = "--"
        self.presrise   = "--"
        self.visibility = "--"
        self.sunrise    = "--"
        self.sunset     = "--"
    
    def __repr__(self):
        return repr((self.condition, self.high, self.low, self.curtemp, self.date, self.day, self.code, self.imageurl, self.pcntprecip))


class Forecasts:
    def __init__(self):
        self.url       = ""
        self.location  = location.Location()
        self.units     = {}
        self.forecasts = []
        self.numfcasts = 0
        self.jsondata  = {}

    def setLocationData(self,opts):
        if opts.locgrabber or opts.locfeeder:
            self.location.getLocation(opts)
        else:
            # DO NOTHING
            return

    def getData(self,opts):
        # GET THE URL DATA
        if self.url != '':
            urld = urllib2.urlopen(self.url)
            
            # READ THE JSON SHENANIGANS
            lines = urld.read()
            if opts.debug:
                print "\n** lines after reading url data **"
                print lines
                print DEBUGSPACER
 
            # CLOSE THE WEB PAGE
            urld.close()
        
            # REMOVE INVALID VARIABLES IF THEY EXIST
            lines = lines.replace('\n','')
            lines = lines.replace('null','"null"')
        
            # SET THE CLASS VARIABLE FOR JSON DATA
            #self.jsondata = ast.literal_eval(lines)
            self.jsondata = json.loads(lines)
            if opts.debug:
                print "\n** actual jsondata dictionary"
                print self.jsondata
        else:
            print "*** NO URL CREATED, PLEASE CALL setURL() PRIOR TO CALLING getJSON() ***"
