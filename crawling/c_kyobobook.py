from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

from selenium import webdriver
import time


def getKyoboBestsellerTitles():
    wd = webdriver.Chrome()  # 크롬 드라이버 실행
    results = []
    for page in range(1, 11):  # 베스트셀러 페이지가 10개까지 있음
        url = f'https://product.kyobobook.co.kr/bestseller/online?period=001&page={page}'
        wd.get(url)  # 페이지 로드
        time.sleep(2)  # 동적 컨텐츠 로딩을 위해 대기
        try:
            html = wd.page_source  # 웹페이지의 소스코드 가져오기
            soupCB = BeautifulSoup(html, 'html.parser')  # 파싱

            titles = soupCB.select("a.prod_info ")  # 제목이 있는 a 태그 찾기


            for i in range(len(titles)):
                title_text = titles[i].get_text(strip=True)
                # print(title_text)
                results.append([title_text])  # 저자 정보를 포함하지 않으므로 리스트에 제목만 추가

        except:
            continue

    wd.quit()

    return results


def main():
    print('교보문고 베스트셀러 크롤링 시작>>>>>>>>')
    results = getKyoboBestsellerTitles()
    for title in results:
        print(title)
    kyobo_table = pd.DataFrame(results, columns=['Title'])  # 데이터 프레임 생성
    kyobo_table.to_csv("./kyobo_bestseller.csv", encoding="utf-8-sig", mode='w', index=False)  # csv 파일 저장, 인덱스 제외

    print('크롤링 완료')


if __name__ == '__main__':
    main()
