from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import folium
import base64
import datetime

fileName='2020-07-17/test4.jpg'


#---------------------------------------위도 경도 고도 계산
pilImage = Image.open(fileName)
EXIFData = pilImage._getexif()
GPSINFOlist={}

if EXIFData:
    for tag, theValue in EXIFData.items():
        tagValue = TAGS.get(tag,tag)
        GPSINFOlist[tagValue]= theValue
else:
    pass
exifGPS = GPSINFOlist['GPSInfo']

latData = exifGPS[2]    #위도 값 받아오기
lonData = exifGPS[4]    #경도 값 받아오기
Altitude = exifGPS[6]   #고도 값 받아오기

# 위도 경도 계산
Lat = latData[0]+(float(latData[1])/60)+(float(latData[2])/3600)
if exifGPS[1] == 'S': Lat = Lat * -1
Lon = lonData[0]+(float(lonData[1])/60)+(float(lonData[2])/3600)
if exifGPS[3] == 'W': Lon = Lon * -1

print(Lat,Lon,Altitude)

#---------------------------------------위도 경도 고도 계산