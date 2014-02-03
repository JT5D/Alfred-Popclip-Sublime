import tweepy, os, sys, re

# Declare OAuth varibles.
CONSUMER_KEY = '...'
CONSUMER_SECRET = '...'
ACCESS_KEY = '...'
ACCESS_SECRET = '...'
keyfile = "authkeys.dat"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Break string into multiple lines
def para(text):
    return reduce(lambda line, word, width=50: '%s%s%s' %(line, ' \n'[(len(line)-line.rfind('\n')-1
    + len(word.split('\n',1)[0]) >= 50)], word), text.split(' '))

# Convert html entities into Unicode
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text
    return re.sub("&#?\w+;", fixup, text)

# Script
type = api.home_timeline(count=30)
for result in type:
                if result.text.find('@')==-1 and result.text.find('http://')==-1:
                        twtu = result.user.screen_name
                        twtt = result.text
                        print para(unescape(twtt)) + "\n" + "\n- " + twtu
                        break