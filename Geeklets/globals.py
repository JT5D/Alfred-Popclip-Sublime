""" GLOBALS
 ROBERT WOLTERMAN (xtacocorex) - 2012

 GLOBAL VARIABLES REQUIRED FOR USE BY THE ULTIMATE WEATHER SCRIPT
"""

# CHANGELOG
# 21 APRIL 2012
#  - EXTRACTION FROM THE MAIN SCRIPT AND PUT INTO THE SERVICES MODULE

# MODULE IMPORTS
import os

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  ***                 ONLY MODIFY THIS SECTION                 ***
# FILE FOR WHERE THE WOEID TO ZIPCODE MAP GOES
# CURRENTLY SET TO BE A HIDDEN FOLDER IN THE USERS HOME DIRECTORY
# YOU CAN CUSTOMIZE THIS IF YOU WANT THE FILE SOMEPLACE ELSE
FCASTLOCDATA = os.getenv('HOME') + os.path.sep + ".zip_woeid_locid_map.txt"
IMAGESAVELOCATION = "/tmp"
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

DEBUGSPACER = "============================================================"
YQLBASEURL = "http://query.yahooapis.com/v1/public/yql"
YQLFORMAT1  = "json"
YQLFORMAT2  = "xml"

IPGRABURLS = {
              'ipinfodb'       : 'http://ipinfodb.com/my_ip_location.php'
              #'ipfingerprints' : 'http://ipfingerprints.com/geolocation.php'
              }

WEATHERSERVICES = [
               'yahoo',
               'weatherchannel',
               'wunderground',
               'weatherbug',
               'usnws',
               'accuweather'
               ]

# CONSTANTS - FOR USE WITH THE myencode()
COMMA     = "%2C"
SPACE     = "%20"
EQUAL     = "%3D"
QUOTE     = "%22"
SEMICOLON = "%3A"
SLASH     = "%2F"
PLUS      = "%2B"
QUESTION  = "%3F"
AMPERSAND = "%26"
RBRACKET  = "%5B"
LBRACKET  = "%5D"
AT        = "%40"
PIPE      = "%7C"

# US STATE TO STATE ABBREVIATION DICTIONARY
USSTATEMAP = {
"Alabama"              : "AL",
"Alaska"               : "AK",
"Arizona"              : "AZ",
"Arkansas"             : "AR",
"California"           : "CA",
"Colorado"             : "CO",
"Connecticut"          : "CT",
"Delaware"             : "DE",
"District of Columbia" : "DC",
"Florida"              : "FL",
"Georgia"              : "GA",
"Hawaii"               : "HI",
"Idaho"                : "ID",
"Illinois"             : "IL",
"Indiana"              : "IN",
"Iowa"                 : "IA",
"Kansas"               : "KS",
"Kentucky"             : "KY",
"Louisiana"            : "LA",
"Maine"                : "ME",
"Maryland"             : "MD",
"Massachusetts"        : "MA",
"Michigan"             : "MI",
"Minnesota"            : "MN",
"Mississippi"          : "MS",
"Missouri"             : "MO",
"Montana"              : "MT",
"Nebraska"             : "NE",
"Nevada"               : "NV",
"New Hampshire"        : "NH",
"New Jersey"           : "NJ",
"New Mexico"           : "NM",
"New York"             : "NY",
"North Carolina"       : "NC",
"North Dakota"         : "ND",
"Ohio"                 : "OH",
"Oklahoma"             : "OK",
"Oregon"               : "OR",
"Pennsylvania"         : "PA",
"Rhode Island"         : "RI",
"South Carolina"       : "SC",
"South Dakota"         : "SD",
"Tennessee"            : "TN",
"Texas"                : "TX",
"Utah"                 : "UT",
"Vermont"              : "VT",
"Virginia"             : "VA",
"Washington"           : "WA",
"West Virginia"        : "WV",
"Wisconsin"            : "WI",
"Wyoming"              : "WY"
             }

