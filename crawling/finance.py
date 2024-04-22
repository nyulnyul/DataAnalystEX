import pandas as pd
import requests
from bs4 import BeautifulSoup

#code1
def get_top100(top100_url, top100_name):
    url = 'https://finance.naver.com/sise/sise_quant.naver'
    result = requests.get(url)
    html = BeautifulSoup(result.content, 'html.parser')
    top100 = html.find_all('a', {'class':'title'})
    for i in range(100):
        url = 'https://finance.naver.com' + top100[i]['href']
        top100_url.append(url)

        company_name = top100[i].string
        top100_name.append(company_name)

    return(top100_url, top100_name)

#code2
def get_company(top100_name):
    company_name = input('주가를 검색할 기업이름을 입력하세요 : ')

    for i in range(100):
        if company_name == top100_name[i]:
            return i
    return 100

#code3
def get_company_stockPage(company_url) :
    result = requests.get(company_url)
    company_stockPage = BeautifulSoup(result.content, 'html.parser')
    return company_stockPage

#code4
def get_price(company_url):
    company_stockPage = get_company_stockPage(company_url)
    no_today = company_stockPage.find('p', {'class':'no_today'}).find('span', {'class':'blind'}).text
    now_price = no_today.find('span', {'class':'blind'}).text
    return now_price

#code0
def main():
    top100_url =[]
    top100_name = []
    b_top100 = True

    top100_url,top100_name  = get_top100(top100_url, top100_name) #code1

    print('네이버 주식 사이트 인기검색 종목 100위')
    print(top100_name)
    print('')

    while b_top100:
        company = get_company(top100_name)
        if company == 100:
            print('해당 기업이 없습니다.')
            b_top100 = False

        else:
            now_price = get_price(top100_url[company])
            print('%s 기업의 현재 주가는 %s 원 입니다.'%(top100_name[company], now_price))
            b_top100 = True

if __name__ == '__main__':
    main()