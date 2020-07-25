import binascii
import os
import sys
def carving(filename):
    EIP=0       #데이터 포인터
    readsize=32 #한 번에 읽을 byte 크기
    Flag=0
    Filesize= os.stat(filename).st_size #파일의 크기를 구함
    f=open(filename,"rb")	#대상 파일 open
    set=''      #데이터 임시 저장 변수
    filename = filename.split('/')[1]
    filename = filename.split('.')[0]
    index=''
    inc=0;
    while EIP<Filesize: #읽어들일 포인터크기가 Filesize를 넘을 때 까지 반복
        Buffer = f.read(readsize)       #변수에 데이터 저장
        data = binascii.b2a_hex(Buffer)  # Buffer의 값을 ASCII 값으로 변경, 시그니처 값 비교 위함
        if Flag:        #Flag 값이 1이면 데이터를 입력한다.
            if Buffer.find(b'\xff\xd9')!=-1:  #읽어온 값이 트레일러 일 경우 파일 1개 쓰기 종료
                temp = int((data.decode('utf-8').find("ffd9"))/2)
                ResultFile.write(Buffer[:temp+2])
                inc+=1
                index='['+str(inc)+']'
                Flag=0
                ResultFile.close()
            else:
                ResultFile.write(Buffer)
        if Flag==0:    #읽어온 값이 헤더 시그니처이면 Flag 값을 1로 설정하고 데이터 작성
            if Buffer.find(b'\xff\xd8\xff')!=-1:
                ResultFile = open("Carving result/" + filename + index+'.jpeg', "wb")
                temp=int((data.decode('utf-8').find("ffd8ffe"))/2)     #헤더 시그니처가 읽어온 문자열의 중간에 있을 경우 그 부분부터 반환
                ResultFile.write(Buffer[temp:])
                Flag=1
                set=''
            else:                               #32byte 마다 읽어들이는데 시그니처가 32byte와 다음 32byte 사이에 끼여있는 경우 방지
                set+=data.decode('utf-8')
                if set.find("ffd8ffe")!=-1:
                    ResultFile = open("Carving result/" + filename + index+'.jpeg', "wb")
                    temp=int(set.find("ffd8ffe"))
                    ResultFile.write(binascii.a2b_hex(set[temp:]))
                    Flag=1
                    set=''
        EIP+=readsize # EIP는 다음 사이즈를 읽기 위해 이동
    f.close()
if len(sys.argv)==0 :
    print('Input argument')
elif len(sys.argv)>2:
    print('Input only one argument')
else:
    path_dir = sys.argv[1]    #대상 폴더 명 지정
    file_list = os.listdir(path_dir)    #디렉터리 내에 존재하는 파일목록을 변수에 저장
    print('Carving file list')
    print(file_list)
    if not os.path.isdir("Carving result") : os.mkdir("Carving result") #결과 디렉토리가 없으면 생성
    for i in range (0,len(file_list)):      #파일의 목록들에 대해 jpeg 카빙 수행
        carving(path_dir+'/'+file_list[i])