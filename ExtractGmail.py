import os
import email
import imaplib
import configparser
import datetime

# 문자열의 인코딩 정보 추출 후, 문자열, 인코딩 얻기
def find_encoding_info(txt):
    info = email.header.decode_header(txt)
    s, encoding = info[0]
    return s, encoding

# gmail imap 세션 생성
session = imaplib.IMAP4_SSL('imap.gmail.com')

# 로그인
session.login('user@gmail.com','password')

# 받은편지함
session.select('Inbox')

# 받은 편지함 내 안 읽은 메일 검색 모든:ALL
result, data = session.search(None, 'UNSEEN')

# 여러 메일 읽기
all_email = data[0].split()

URLlist=[]  #본문 데이터가 모두 저장될 리스트
for mail in all_email:
    result, data = session.fetch(mail, '(RFC822)')
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    # 메일 정보

 #   subject, encode = find_encoding_info(email_message['Subject'])
    #print('[Message]')
    message='' #메일 본문 데이터가 저장될 변수
    # 메일 본문 확인
    if email_message.is_multipart():
        for part in email_message.get_payload():
            if part.get_content_type() == 'text/plain':
                bytes = part.get_payload(decode=True)
                encode = part.get_content_charset()
                message = message + str(bytes, encode)
                message.rstrip('\n')
                URLlist.append(message)
    else:
        if email_message.get_content_type() == 'text/plain':
            bytes = email_message.get_payload(decode=True)
            encode = email_message.get_content_charset()
            message = str(bytes, encode)
            print('debug')
    print(message)