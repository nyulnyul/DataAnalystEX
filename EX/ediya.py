from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

def best_seller(result):

    for page in range(1,21):
        url = f'https://aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=0&page={page}&cnt=1000&SortOrder=1'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tag_tbody = soup.find('tbody')
        for book in tag_tbody.find_all('tr'):
            if len(book) <= 1:
                break
            book_td = book.find_all('td')
            book_title = book_td[1].find('a.bo3').get_text(strip=True)

            book_author = book_td[2].get_text(strip=True)
            book_publisher = book_td[3].get_text(strip=True)
            book_date = book_td[4].get_text(strip=True)

            result.append([book_title, book_author, book_publisher, book_date])

    return

def main():
    result = []
    print('Aladin best seller crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    best_seller(result)

    print(f'Total books: {len(result)}')
    if result:
        print('First book:', result[0])
        print('Last book:', result[-1])

    best_seller_tbl = pd.DataFrame(result, columns=('Title', 'Author', 'Publisher', 'Date'))
    best_seller_tbl.to_csv('best_seller.csv', encoding='utf-8', mode='w', index=False)
    del result[:]

if __name__ == '__main__':
    main()
