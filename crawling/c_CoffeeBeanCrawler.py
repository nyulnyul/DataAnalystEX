from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

from selenium import webdriver
import time

#[CODE 1]
def CoffeeBean_store(result): #커피빈 매장 크롤링
    CoffeeBean_URL = "https://www.coffeebeankorea.com/store/store.asp" #커피빈 매장 주소 URL
    wd = webdriver.Chrome() #크롬 브라우저 실행
    storeCnt = 0  #매장 수
             
    for i in range(1, 10):  #마지막 매장번호(최근 신규 매장번호) 까지 반복
        wd.get(CoffeeBean_URL) #url을 호출하여 응답을 받아옴
        time.sleep(1)  #웹페이지 연결할 동안 1초 대기
        try:
            wd.execute_script("storePop2(%d)" %i) #매장 상세정보가 있는 팝업 화면 호출
            time.sleep(1) #스크립트 실행 할 동안 1초 대기
            html = wd.page_source #웹페이지의 소스코드 가져오기
            soupCB = BeautifulSoup(html, 'html.parser') #파싱
            store_name_h2 = soupCB.select("div.store_txt > h2") #매장 이름이 있는 h2 태그 찾기
            store_name = store_name_h2[0].string #매장 이름 가져오기
            store_info = soupCB.select("div.store_txt > table.store_table > tbody > tr > td") #매장 정보가 있는 table 태그 찾기
            store_address_list = list(store_info[2]) #매장 주소가 있는 td 태그 찾기
            store_address = store_address_list[0] #매장 주소 가져오기
            store_phone = store_info[3].string #매장 전화번호
            result.append([str(i)]+[store_name]+[store_address]+[store_phone]) #데이터 프레임 구조 #리스트에 추가
            print("%s %s" %(str(i), store_name))  #매장 이름 출력하기

            storeCnt += 1 #매장 수 증가
        except:
            continue

    return storeCnt #매장 수 반환

#[CODE 0]
def main(): #메인 함수
    result = [] #크롤링 결과 저장할 리스트
    Cnt = 0 #매장 수

    print('CoffeeBean store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>') #출력
    Cnt = CoffeeBean_store(result)  #[CODE 1] 호출 #커피빈 매장 크롤링
    print("총 매장 수 : %d" %Cnt) #매장 수 출력
    
    CB_tbl = pd.DataFrame(result, columns=('no', 'store', 'address','phone'))   #데이터 프레임 구조
    CB_tbl.to_csv('./CoffeeBean.csv', encoding='cp949', mode='w', index=True) #csv 파일로 저장

if __name__ == '__main__':
     main()

