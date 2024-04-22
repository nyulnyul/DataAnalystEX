from bs4 import BeautifulSoup
import pandas as pd
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def Starbucks_store(result):
    Starbucks_URL = 'https://www.starbucks.co.kr/store/store_map.do'
    wd = webdriver.Chrome()  # Chrome 드라이버 생성
    wd.get(Starbucks_URL)  # 스타벅스 매장 찾기 페이지 접속
    time.sleep(5)  # 페이지 로딩 대기

    for i in range(1, 10):  # 시도 선택 (임의로 10개 지역만 선택)
        try:
            # 시도 선택
            sido_button = wd.find_element(By.CLASS_NAME, "sido_arae_box")
            sido_li = sido_button.find_elements(By.TAG_NAME, "li")
            sido_li[i].click()
            time.sleep(2)

            # 구군 선택 (여기서는 첫 번째 구군만 선택)
            gugun = wd.find_element(By.CLASS_NAME, 'gugun_arae_box')
            li = gugun.find_elements(By.TAG_NAME, 'li')
            li[0].click()  # 첫 번째 구군 선택
            time.sleep(2)

            # 매장 정보 가져오기
            store_list = wd.find_elements(By.CSS_SELECTOR, 'ul.quickSearchResultBoxSidoGugun > li')

            for store in store_list:
                store_name = store.find_element(By.TAG_NAME, 'strong').text
                store_info = store.find_element(By.TAG_NAME, 'p').text.split('\n')
                if len(store_info) >= 2:
                    store_address = store_info[0]
                    store_phone = store_info[1]
                else:
                    store_address = store_info[0]
                    store_phone = ''
                result.append([store_name, store_address, store_phone])
                print(f"{len(result)} {store_name}")  # 매장 수와 매장 이름 출력
        except Exception as e:
            print(f"Error: {e}")
            continue

    wd.close()  # 브라우저 닫기
    return len(result)  # 총 매장 수 반환


def main():
    result = []

    print('Starbucks store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    count = Starbucks_store(result)
    print("총 매장 수 :", count)

    SB_tbl = pd.DataFrame(result, columns=('store', 'address', 'phone'))
    SB_tbl.to_csv('./Starbucks.csv', encoding='utf-8', mode='w', index=True)


if __name__ == "__main__":
    main()
