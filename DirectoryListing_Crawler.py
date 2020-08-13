import urllib
from bs4 import BeautifulSoup
import os
from urllib.request import urlretrieve
def download(link):
    url = link
    soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    for link in soup.findAll("a"): # a 태그를 찾습니다
        if 'href' in link.attrs:  # 내부에 있는 항목들을 리스트로 가져옵니다
            if link.attrs['href'] == '/' or '/assets/' in link.attrs['href'] or link.attrs['href'][0] == '?': # 탐색할 필요없는 링크 예외처리
                continue

            if link.attrs['href'][-1] == '/':   #또 다른 폴더일 경우 재귀함수로 모두 탐색
                download(url + link.attrs['href'])
            else:
                filename = 'result/' + link.attrs['href']   #파일명 지정
                print(url+link.attrs['href'])   #경로 출력
                urlretrieve(url+link.attrs['href'],filename)    #파일 다운로드
if os.path.isdir('result'):
    pass
else:
    os.makedirs(os.path.join('result'))
download('URL')