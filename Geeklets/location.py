""" location
 ROBERT WOLTERMAN (xtacocorex) - 2012

 LOCATION CLASSES:
  - IPINFODB INHERITS SGML PARSER AND PARSES THE HTML DATA FROM THAT WEBSITE TO OBTIAN LOCATION BASED OPON IP
  - Location STORES ALL OF THE LOCATION DATA FOR THE SCRIPT, THIS IS A MEMBER VARIABLE TO forecasts.Forecast
"""

# CHANGELOG
# 21 APRIL 2012
#  - EXTRACTION FROM THE MAIN SCRIPT AND PUT INTO THE SERVICES MODULE

# MODULE IMPORTS
import urllib2, re, json
from sgmllib import SGMLParser
from globals import *
from utilityfunctions import *

# CLASSES
# IPINFODB PARSER CLASS
# PARSES THE ipinfodb WEBSITE DATA
class IPINFODB(SGMLParser):
    def reset(self):                              
        SGMLParser.reset(self)
        # SET UP LOCATION DATA DICTIONARY
        self.zipcode            = ""
        self.country            = ""
        self.stprov             = ""
        self.city               = ""
        self.lat                = ""
        self.lon                = ""
        # INITIALIZE inside_xxx_element TO BE FALSE
        self.inside_div_element = False
        self.inside_li_element  = False
        # INITIALIZE LI COUNT
        self.li_count           = 0
        self.done_proc          = False

    def start_div(self, attrs):                     
        # SINCE WE'RE IN A div TAG, SET OUR inside_div_element TO TRUE
        # IF WE ARE IN THE CLASS section
        if attrs[0][0] == 'class' and attrs[0][1] == 'section':
            self.inside_div_element = True
            self.done_proc          = False
        
    def start_li(self, attrs):              
        # FIGURE OUT IF WE ARE IN THE LI TAG WE WANT
        if self.inside_div_element:
            self.inside_li_element = True
        
        # IF WE ARE INSIDE THE LI WE WANT, INCREMENT OUR COUNTER
        if self.inside_li_element and not self.done_proc:
            self.li_count += 1
            
        # FIGURE OUT IF WE NEED TO STOP COUNTING
        if self.li_count == 8:
            self.done_proc = True
    
    def handle_data(self, text):       
        # DETERMINE IF WE'RE IN THE LI WE WANT
        if self.inside_li_element:
            
            # FIGURE OUT IF WE ARE ABOVE AN LI COUNT OF 1 AND STILL PROCESSING
            if self.li_count > 1 and not self.done_proc:
                # IF SO, STRIP OFF EVERYTHING TO THE RIGHT AND LEFT OF THE TEXT
                tmp = text.lstrip().rstrip()
                # SPLIT ON THE DELIMETER BETWEEN THE FIELD AND THE DATA
                tmp = tmp.split(" : ")
                
                # FIGURE OUT WHAT WE ARE LOOKING AT
                if   self.li_count == 2:
                    self.country = tmp[1].lower()
                elif self.li_count == 3:
                    self.stprov  = tmp[1].lower()
                elif self.li_count == 4:
                    self.city    = tmp[1].lower()
                elif self.li_count == 5:
                    self.zipcode = tmp[1]
                elif self.li_count == 6:
                    self.lat     = tmp[1]
                elif self.li_count == 7:
                    self.lon     = tmp[1]

    def end_div(self):
        # SINCE WE'RE EXITING AN A TAG, SET OUR inside_div_element TO FALSE
        self.inside_div_element = False

    def end_li(self):
        # SINCE WE'RE EXITING AN A TAG, SET OUR inside_li_element TO FALSE
        self.inside_li_element = False

class Location:
    def __init__(self):
        self.zipcode = ""
        self.country = ""
        self.stprov  = ""
        self.city    = ""
        self.lat     = ""
        self.lon     = ""
        self.woeid   = ""
        self.locid   = ""
    
    def __str__(self):
        return "%s %s" % (self.stprov,self.city)
    
    def getLocation(self,opts):
        """
            getLocation()
             - GETS THE LOCATION DATA
             - INPUT:  opts - COMMAND LINE OPTIONS
             - OUPUTS: NONE
        """
        if opts.locgrabber:
            # GET THE URL FROM THE IPGRABURLS DICTIONARY
            req  = urllib2.Request(IPGRABURLS[opts.locserv])
            urld = urllib2.urlopen(req)
            # READ THE WEB PAGE
            lines = urld.read()
            if opts.debug:
                print lines
                print DEBUGSPACER
            # CLOSE THE WEB PAGE
            urld.close()
            
            # FIGURE OUT WHICH LOCATION SERVICE WE ARE USING
            if   opts.locserv == 'ipinfodb':        
                # CREATE OUR LOCATION PARSER
                locparser = IPINFODB()
                locparser.feed(lines)
            #elif opts.locserv == 'ipfingerprints':
            #    print "nothing"
            #    locparser = None
        
            # GET LOCATION DATA FROM THE PARSER
            self.zipcode = locparser.zipcode
            self.country = locparser.country
            self.stprov  = locparser.stprov
            self.city    = locparser.city
            self.lat     = locparser.lat
            self.lon     = locparser.lon
        elif opts.locfeeder:
            # GET LOCATION DATA FROM THE COMMAND LINE ARGUMENTS
            self.zipcode = opts.zipcode
            self.country = opts.country
            self.stprov  = opts.stateprov
            self.city    = opts.city
            self.lat     = "--"
            self.lon     = "--"
        else:
            # DO NOTHING
            return
        
        # NOW GET THE IDS
        # THIS WILL ALSO GET LAT/LON INFORMATION IF opts.locfeeder IS SET
        self.__getIDs(opts)
        
        # DEBUG
        if opts.debug:
            print "** location information"
            print "lat: %s\nlon: %s" % (self.lat,self.lon)
    
    def __getIDs(self,opts):
        """
            __getIDs
             - FUNCTION TO GET THE WOEID ID AND LOCATION ID FROM THE LOCALLY STORED DATABASE
              OR
               PULLS THE DATA FROM THE INTERNET AND STORES INTO THE DATABASE
             - THIS FUNCTION WILL ALSO GRAB THE LATITUDE AND LONGITUDE FOR THE LOCATION
               IF opts.locfeeder IS SET (USER INPUT LOCATION, CURRENT NO SUPPORT FOR LAT/LON CLI)
             - INPUT:  opts    - COMMAND LINE OPTIONS
             - OUPUTS: NONE
        """
        
        # CHECK TO SEE IF THE ZIP IS IN THE FILE
        haveIDs   = False
        haveFile  = False
        if os.path.isfile(FCASTLOCDATA):
            if opts.debug:
                print "*** using local file for WOEID grab: %s" % FCASTLOCDATA
            fin = open(FCASTLOCDATA,'r+a')
            haveFile = True
        else:
            # WE HIT THE CASE WHERE THE FILE DOESN'T EXIST
            if opts.debug:
                print "*** creating zipcode, woeid, and locid map: %s" % FCASTLOCDATA
            fin = open(FCASTLOCDATA,'w')
            haveFile = False
            
        # IF WE HAVE THE INPUT FILE, LOOK FOR OUR ZIPCODE
        if haveFile:
            # LOOP THROUGH THE LINES
            for line in fin.readlines():
                if opts.debug:
                    print "line: ", line
                if self.zipcode in line:
                    # GET THE WOEID AND RIGHT STRIP TO REMOVE THE RETURN LINE FROM THE FILE
                    tmp = line.split(",")
                    self.woeid = tmp[1].rstrip()
                    self.locid = tmp[2].rstrip()
                    # GET THE LAT AND LON IF WE ARE USING THE LOCFEEDER
                    if opts.locfeeder:
                        yqlquery = 'select centroid from geo.places where woeid=\"%s\" limit 1' % self.woeid
                        LATLONURL = YQLBASEURL + "?q=" + myencode(yqlquery) + "&format=" + YQLFORMAT1
                        # GET THE DATA FROM THE INTERNETS
                        reqresp = urllib2.urlopen(LATLONURL)
                        # NEED TO BREAK THE STRING INTO THE APPROPRIATE DICTIONARY STRUCTURE
                        resp    = json.loads(reqresp.read())
                        reqresp.close()
                        self.lat = resp['query']['results']['place']['centroid']['latitude']
                        self.lon = resp['query']['results']['place']['centroid']['longitude']
                    # NOT RETURNING HERE SO WE CAN GRACEFULLY CLOSE THE INPUT FILE
                    # THIS IS A STUPID LITTLE ISSUE
                    haveIDs = True
                    # FIXED BUG HERE THAT WOULD CAUSE THE ZIP/WOEID TO GET
                    # RE-ADDED TO THE MAPPING FILE HERE BECAUSE I DIDN'T BREAK
                    # FROM THE LOOP
                    break
                else:
                    haveIDs = False
    
        # IF WE DON'T HAVE THE WOEID, LET'S GET THE SHIZZLE AND STORE LOCALLY
        if not haveIDs:
            if opts.debug:
                print "*** obtaining data from the internet"
            
            # GET THE STRING WITH ALL OF THE DATA ENCODED WITH +
            fulllocstr1 = self.city+","+self.stprov+" "+self.zipcode+" "+self.country
            if self.country == "united states":
                fulllocstr2 = "%s+%s+%s" % (self.city.replace(" ","+"),self.stprov.replace(" ","+"),self.country.replace(" ","+"))
            else:
                fulllocstr2 = "%s+%s" % (self.city.replace(" ","+"),self.country.replace(" ","+"))
        
            # ****************** WOEID ******************
            # GET THE URL TO FIND WOEID
            if opts.yql_loc_type == 'zip':
                yqlquery = 'select woeid,centroid from geo.places where text=\"%s\" limit 1' % self.zipcode
            elif opts.yql_loc_type == 'full':
                yqlquery = 'select woeid,centroid from geo.places where text=\"%s\" limit 1' % fulllocstr1
            WOEIDURL = YQLBASEURL + "?q=" + myencode(yqlquery) + "&format=" + YQLFORMAT1
            if opts.debug:
                print "*** woeid"
                print yqlquery
                print WOEIDURL
                print DEBUGSPACER
            
            # GET THE DATA FROM THE INTERNETS
            reqresp = urllib2.urlopen(WOEIDURL)
            
            # NEED TO BREAK THE STRING INTO THE APPROPRIATE DICTIONARY STRUCTURE
            #resp    = ast.literal_eval(reqresp.read())
            resp    = json.loads(reqresp.read())
            reqresp.close()
            
            # SEARCH THE RESPONSE FOR THE WOEID
            # JSON IS AWESOME! YAY FOR NESTED DICTIONARIES
            self.woeid = resp['query']['results']['place']['woeid']
            # HERE WE WILL GET THE LATITUDE AND LONGITUDE IF WE ARE FEEDING IN A LOCATION
            if opts.locfeeder:
                self.lat = resp['query']['results']['place']['centroid']['latitude']
                self.lon = resp['query']['results']['place']['centroid']['longitude']
            
            # ****************** LOCID ******************
            # GET THE URL TO FIND LOCID
            QUERYHEAD = 'select id from xml where url="http://xoap.weather.com/search/search?where='
            QUERYFOOT = '"and itemPath="search.loc" limit 1'
            if opts.yql_loc_type == 'zip':
                yqlquery = QUERYHEAD + "%s" + QUERYFOOT % self.zipcode
            elif opts.yql_loc_type == 'full':
                yqlquery = QUERYHEAD + fulllocstr2 + QUERYFOOT
            LOCIDURL = YQLBASEURL + "?q=" + myencode(yqlquery) + "&format=" + YQLFORMAT1
            if opts.debug:
                print "*** locid"
                print yqlquery
                print LOCIDURL
                print DEBUGSPACER
            # GET THE DATA FROM THE INTERNETS
            reqresp = urllib2.urlopen(LOCIDURL)
            
            # NEED TO BREAK THE STRING INTO THE APPROPRIATE DICTIONARY STRUCTURE
            resp    = json.loads(reqresp.read())
            reqresp.close()
            
            # SEARCH THE RESPONSE FOR THE WOEID
            # JSON IS AWESOME! YAY FOR NESTED DICTIONARIES
            self.locid = resp['query']['results']['loc']['id']
            
            # WRITE THE DATA TO THE FILE
            fmt = "%s,%s,%s\n" % (self.zipcode,self.woeid,self.locid)
            fin.write(fmt)
            
        # NOW WE CAN CLOSE THE FILE
        fin.close()
    
    def getLatLon(self):
        return (self.lat,self.lon)
    
    def getAllLocData(self):
        return (self.zipcode,self.country,self.stprov,self.city,self.lat,self.lon,self.woeid,self.locid)
