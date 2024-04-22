import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from itertools import count

import ssl   #접속보안 허용

#[CODE1]

# [CODE0]
def main():  # 교촌치킨 매장 주소 크롤링 메인 함수
    result = []  # 크롤링 결과 저장할 리스트

    print('bbq ADDRESS CRAWLING START>>>>>>>>')  # 크롤링 시작 메시지 출력
    getKyochonAddress(result)  # [CODE2] 교촌치킨 매장 주소 크롤링

    kyochon_table = pd.DataFrame(result,
                                 columns=('no', 'store', 'sido_gungu', 'store_address', 'store_phone'))  # 데이터 프레임 생성
    kyochon_table.to_csv("./kyochon.csv", encoding="cp949", mode='w', index=True)  # csv 파일 저장
    del result[:]  # 크롤링 결과 리스트 초기화

    print('FINISHED')  # 크롤링 완료 메시지 출력


if __name__ == '__main__':  # 메인 함수
    main()


