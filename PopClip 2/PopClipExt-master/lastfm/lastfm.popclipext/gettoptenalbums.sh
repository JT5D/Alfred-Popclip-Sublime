APIKEY="46fa5b47994319641d2893804c2a5c11"
LOCATION="/Users/$USER/Documents"  
POPCLIP_TEXT="Europe"
POPCLIP_TEXT=`echo $POPCLIP_TEXT | gsed 's/ /+/g'`

curl http://ws.audioscrobbler.com/2.0/\?method\=artist.gettopalbums\&artist\=$POPCLIP_TEXT\&api_key\=46fa5b47994319641d2893804c2a5c11 > $LOCATION/temporary

RESULT=`perl -p -e 's/\n//' "$LOCATION/temporary" | gsed -e "s/<album/\n\<album/g" | grep \<album | gsed -e "s/.*<name>\([^<]*\)<\/name>.*<playcount.*\"extralarge\">\([^<]*\)<\/image>.*/[\1](\2)  /" | head -n 10`

printf "$RESULT"
 

