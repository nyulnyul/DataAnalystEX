from bs4 import BeautifulSoup
import requests
import pandas as pd
import ssl


def webtoon_list(result):
    ssl._create_default_https_context = ssl._create_unverified_context  # 접속보안 허용
    headers = {'User-Agent': 'Mozilla/5.0'}
    for page in range(1, 10):  # 1페이지부터 9페이지까지 크롤링
        url = f'https://comic.naver.com/webtoon/list?titleId=737628&page={page}&sort=DESC&tab=sun'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.txt, 'html.parser')

        tbody = soup.find('table', class_='viewList').tbody
        for tr in tbody.find_all('tr', class_=lambda x: x != 'band_banner'):  # 광고 배너를 제외한 에피소드 목록 가져옴
            # 에피소드 제목과 날짜를 추출합니다.
            title = tr.find('td', class_='title').find('a').get_text(strip=True)
            date = tr.find('td', class_='num').get_text(strip=True)

            result.append([title, date])
    return


def main():
    result = []
    print('Naver webtoon crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    webtoon_list(result)

    print(f'Total episodes: {len(result)}')
    if result:
        print('First episode:', result[0])
        print('Last episode:', result[-1])

    webtoon_tbl = pd.DataFrame(result, columns=('Episode Title', 'Date'))
    webtoon_tbl.to_csv('webtoon.csv', encoding='utf-8', mode='w', index=False)
    del result[:]


if __name__ == '__main__':
    main()
