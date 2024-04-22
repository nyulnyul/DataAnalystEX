from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime
import ssl

#[CODE 1]
def hollys_store(result): #할리스 매장 크롤링
    # SSL 인증서 검증 무시(맥북만)
    ssl._create_default_https_context = ssl._create_unverified_context # 접속보안 허용

    for page in range(1,59): #매장 페이지가 58개까지 있음
        i = 0 #페이지별 매장 수
        Hollys_url = 'https://www.hollys.co.kr/store/korea/korStore.do?pageNo=%d&sido=&gugun=&store=' %page #할리스 매장 주소 URL

        html = urllib.request.urlopen(Hollys_url) #url을 호출하여 응답을 받아옴
        soupHollys = BeautifulSoup(html, 'html.parser') #파싱 #html.parser를 사용해서 soup에 넣겠다

        #response = requests.get(Hollys_url) # urllib.request를  get으로 바꿔보기
        # soupHollys = BeautifulSoup(response.txt, 'html.parser')

        tag_tbody = soupHollys.find('tbody') #tbody 찾아옴 #매장 정보가 있는 tbody 태그 찾기
        for store in tag_tbody.find_all('tr'): # tr 태그 내용을 가져옴
            if len(store) <= 3: #매장 정보가 없는 경우
                break
            
            store_td = store.find_all('td') # td 태그 내용을 가져옴
            store_name = store_td[1].string #가져오려는 값만 #매장 이름
            store_sido = store_td[0].string #시도
            store_address = store_td[3].string #주소
            store_phone = store_td[5].string #전화번호
            i += 1 #페이지별 매장 수
            no = "{0:0>3}-{1:0>3}".format(str(page), str(i)) #몇번째 페이지인지 확인 위해 추가 #페이지별 매장번호
            result.append([store_name]+[store_sido]+[store_address]+[store_phone]+[no]) #데이터 프레임 구조 #리스트에 추가

        print(Hollys_url, no) #중간 확인용 출력
    return

#CODE 0]
def main(): #메인 함수
    result = [] #크롤링 결과 저장할 리스트
    print('Hollys store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>') #출력
    hollys_store(result)   #[CODE 1] 호출 #할리스 매장 크롤링
    print(len(result)) #매장 수 출력
    print(result[0]) #첫번째 매장 정보 출력
    print(result[(len(result) -1)]) #마지막 매장 정보 출력
    
    hollys_tbl = pd.DataFrame(result, columns=('store', 'sido-gu', 'address','phone', 'no')) #데이터 프레임 구조
    hollys_tbl.to_csv('hollys.csv', encoding='utf-8', mode='w', index=True) #csv 파일로 저장
    del result[:] #크롤링 결과 리스트 초기화
       
if __name__ == '__main__': #메인 함수 호출
     main()
