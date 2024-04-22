from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

from  selenium import webdriver
import time

def dacon_store(result):
    Dacon_URL = 'https://dacon.io/competitions'
    wd = webdriver.Chrome()
    storeCnt = 0

    for i in range(1, 10):
        wd.get(Dacon_URL)
        time.sleep(1)
        try:
            wd.execute_script("official/%s/overview/description" %i)
            time.sleep(1)
            html = wd.page_source
            soupDC = BeautifulSoup(html, 'html.parser')
            store_name1 = soupDC.select("div.CompetitionDetailTitleSection mx-auto px-5 px-md-7 py-6 grey v-sheet theme--light white--text > h2.text-h5 font-weight-bold mb-1")
            store_name = store_name1[0].string
            # store_info = soupDC.select("div.store_txt > table.store_table > tbody > tr > td")
            # store_address_list = list(store_info[2])
            # store_address = store_address_list[0]
            # store_phone = store_info[3].string
            result.append([str(i)]+[store_name])
            print("%s %s" %(str(i), store_name))

            storeCnt += 1
        except:
            continue

    return storeCnt
def main():
    result = []
    Cnt = 0
    print('Dacon store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    Cnt = dacon_store(result)
    print("총 대회 수 : %d" %Cnt)

    DC_tbl = pd.DataFrame(result, columns=('no', 'store'))   #데이터 프레임 구조
    DC_tbl.to_csv('./Dacon.csv', encoding='cp949', mode='w', index=True) #csv 파일로 저장

if __name__ == '__main__':
    main()