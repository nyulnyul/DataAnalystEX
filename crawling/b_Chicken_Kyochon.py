import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from itertools import count

import ssl   #접속보안 허용

#[CODE1]
def get_request_url(url, enc='utf-8'): #API 요청 URL을 호출하여 응답을 받아오는 함수
    
    req = urllib.request.Request(url) #url 요청

    try:
        ssl._create_default_https_context = ssl._create_unverified_context    # [SSL: CERTIFICATE_VERIFY_FAILED]에러 발생시 
        
        response = urllib.request.urlopen(req) #요청한 url을 열어서 response에 저장
        if response.getcode() == 200: #요청이 성공했을 경우
            try:                  
                rcv = response.read() #요청한 url의 내용을 반환
                ret = rcv.decode(enc) #요청한 url의 내용을 반환
            except UnicodeDecodeError: #에러 발생시
                ret = rcv.decode(enc, 'replace')   # 에러발생시 ?로 변경  #요청한 url의 내용을 반환
            
            return ret #요청한 url의 내용을 반환
            
    except Exception as e: #에러 발생시
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url)) #에러 메시지 출력
        return None

#[CODE2]
def getKyochonAddress(result):   # 교촌치킨 매장 주소 크롤링
  
    for sido1 in range(1, 18):           # 전국 시도 
        for sido2 in count(1):           # 구/군   count(1)은 중복 방지위해 1로 해야해서 점점 증가
            Kyochon_URL = 'https://www.kyochon.com/shop/domestic.asp?sido1=%s&sido2=%s&txtsearch=' %(str(sido1), str(sido2)) # 교촌치킨 매장 주소 URL
            print("%d-%d %s" %(sido1, sido2, Kyochon_URL)) # 중간 확인용 출력
            no = "{0:0>3}-{1:0>3}".format(str(sido1), str(sido2)) #몇번째 페이지인지 확인 위해 추가

            try:
                rcv_data = get_request_url(Kyochon_URL) # [CODE1] url을 호출하여 응답을 받아옴
                soupData = BeautifulSoup(rcv_data, 'html.parser') #파싱
    
                ul_tag= soupData.find('ul', attrs={'class': 'list'})    # 매장 정보가 있는 ul 태그 찾기 attrs는 속성값을 찾아줌

                for store_data in ul_tag.findAll('a', href=True):   # a 태그 내에 href가 있는 a태그만 가져와라
                    store_name = store_data.find('strong').get_text() # 매장 이름
                    store_address = store_data.find('em').get_text().strip().split('\r')[0] # 매장 주소
                    store_phone = store_data.find('em').get_text().strip().split('\r')[2].strip() # 매장 전화번호
                    store_sido_gu = store_address.split()[:2] # 매장 주소에서 시도, 구군 추출
                    store_sido_gu1 = '%s %s' %(store_sido_gu[0], store_sido_gu[1]) # 시도, 구군 합치기
                    result.append([no] + [store_name] + [store_sido_gu1] + [store_address] + [store_phone]) # 데이터 프레임 구조
            except:
                break
    return

#[CODE0]
def main():   # 교촌치킨 매장 주소 크롤링 메인 함수
    result = [] # 크롤링 결과 저장할 리스트

    print('KYOCHON ADDRESS CRAWLING START>>>>>>>>') # 크롤링 시작 메시지 출력
    getKyochonAddress(result) # [CODE2] 교촌치킨 매장 주소 크롤링
    
    kyochon_table = pd.DataFrame(result, columns=('no', 'store', 'sido_gungu', 'store_address', 'store_phone')) # 데이터 프레임 생성
    kyochon_table.to_csv("./kyochon.csv", encoding="cp949", mode='w', index=True) # csv 파일 저장
    del result[:]   # 크롤링 결과 리스트 초기화

    print('FINISHED') # 크롤링 완료 메시지 출력
    
if __name__ == '__main__': # 메인 함수
     main()


