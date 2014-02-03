#link='http://srtm.csi.cgiar.org/SRT-ZIP/SRTM_V41/SRTM_Data_GeoTiff'
link='http://droppr.org/srtm/v4.1/6_5x5_TIFs/'
#link='ftp://xftp.jrc.it/pub/srtmV4/tiff/'
for i in {14..72}; 
do
    for j in {01..24}; 
    do 
        rm srtm_$i'_'$j'.zip'
	wget $link/srtm_$i'_'$j'.zip'; 
    done
done
