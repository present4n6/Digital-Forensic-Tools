from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import folium
import os
EXIFlist=[] #각 사진 파일의 데이터를 2차원으로 저장할 리스트
gmaps = "https://www.google.com/maps?q={},{}"   #구글 맵 URL 선언
for root, dirs, files in os.walk('D:\'):    #사진 파일이 있는 폴더의 경로 지정
    for fname in files:     #폴더 내 모든 파일 탐색
        filename = os.path.join(root, fname)    #파일의 경로를 filename 변수에 저장
        try:
            pilImage = Image.open(filename)     #값을 분석할 파일 open
            EXIFData = pilImage._getexif()      #exif 데이터를 가져온다
            GPSINFOlist = {}                    #exif 데이터가 저장될 딕셔너리 형 변수

            if EXIFData:                        #EXIF 데이터가 존재할 경우 값을 가져온다
                for tag, theValue in EXIFData.items():
                    tagValue = TAGS.get(tag, tag)
                    GPSINFOlist[tagValue] = theValue
            else:
                pass
            exifGPS = GPSINFOlist['GPSInfo']    # GPSInfo 그룹 데이터 가져오기
            latData = exifGPS[2]                # 위도 값 가져오기
            lonData = exifGPS[4]                # 경도 값 가져오기
            # 위도 경도를 좌표 값으로 계산
            Lat = latData[0] + (float(latData[1]) / 60) + (float(latData[2]) / 3600)        #위도 값 계산
            if exifGPS[1] == 'S': Lat = Lat * -1
            Lon = lonData[0] + (float(lonData[1]) / 60) + (float(lonData[2]) / 3600)
            if exifGPS[3] == 'W': Lon = Lon * -1

            templist=[]                         # 사진 파일의 데이터 임시 저장 리스트
            templist.append((Image.open(filename)._getexif()[36867]))   # exif 데이터에서 시간 값을 가져오는 함수
            templist.append(Lat)                # 위도 값 추가
            templist.append(Lon)                # 경도 값 추가
            templist.append(filename)           # 파일 명 추가
            EXIFlist.append(templist)           # 해당 파일의 데이터 리스트를 EXIFlist에 추가
        except:                                 # 위도, 경도 값이 없을 경우 None으로 입력
            templist = []
            templist.append((Image.open(filename)._getexif()[36867]))
            templist.append('None')
            templist.append('None')
            templist.append(filename)
            EXIFlist.append(templist)
            pass

EXIFlist=sorted(EXIFlist, key=lambda x: int(x[0].replace(':','').replace(' ','')))  #EXIFlist의 리스트들을 시간 순서대로 정렬
#------------------------------------------------------------------- Google map
m = folium.Map(
    zoom_start=10
)
point=[]            #각 좌표들이 모두 저장될 리스트
for i in range(len(EXIFlist)):  # 모든 좌표 값들을 구글 맵에 표현
    if EXIFlist[i][1]=='None':  # 위도, 경도 값이 없을 경우 pass
        pass
    else:
        print("Google Maps URL: {}".format(gmaps.format(EXIFlist[i][1], EXIFlist[i][2])))   #구글 맵 URL 출력
        locations=[float(EXIFlist[i][1]),float(EXIFlist[i][2])]     # loactions에 좌표 값 저장
        point.append(locations)                                     # 좌표 추가
        folium.Marker(
            location=[EXIFlist[i][1],EXIFlist[i][2]],               #위도, 경도 값 입력
            popup=str(i+1)+'번째\n'+EXIFlist[i][3].split('\\')[-1]+'\n'+EXIFlist[i][0],   #마커를 클릭하면 시간 순서번호, 파일 명, 시간 정보가 출력
            icon=folium.Icon(color='red',icon='ok') #마커 모양 지정
        ).add_to(m)
folium.PolyLine(point, color="blue", weight=2.5, opacity=1).add_to(m)    #각 지점을 파란 선으로 연결
m.save('GPS_location.html')                                         # 결과 파일을 GPS_location.html 로 저장

for i in range(len(EXIFlist)):
    print(EXIFlist[i])