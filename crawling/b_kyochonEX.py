from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime
import ssl
from itertools import count


def get_request_url(url, enc='utf-8'):
  req = urllib.request.Request(url)
  try:

    ssl._create_default_https_context = ssl._create_unverified_context  # 접속보안 허용
    response = urllib.request.urlopen(req)
    if response.getcode() == 200:
      try:
        rcv = response.read()
        ret = rcv.decode(enc)
      except UnicodeDecodeError:

        ret = rcv.decode(enc, 'replace')
      return ret
  except Exception as e:
    print(e)
    print('[%s] Error for URL : %s' % (datetime.datetime.now(), url))
    return None

def getKyochonAddress(sido1, result):
  for sido2 in count(): #중복 방지위해 1로 해야함
    url = 'http://www.kyochon.com/shop/domestic.asp?txtsearch=&sido1=%s&sido2=%s' % (str(sido1), str(sido2))
    print(url)
    try:
      rcv_data = get_request_url(url)
      soupData = BeautifulSoup(rcv_data, 'html.parser')

      ul_tag = soupData.find('ul', attrs={'class': 'list'})

      for store_data in ul_tag.findAll('a', href=True): # a 태그 내에 href가 있는 a태그만 가져와라
        store_name = store_data.find('strong').get_text()
        store_address = store_data.find('em').get_text().strip().split('\r')[0]
        store_phone = store_data.find('em').get_text().strip().split('\r')[2].strip()
        store_sido_gu = store_address.split()[0:2]
        store_sido_gu1 = '%s %s'%(store_sido_gu[0] , store_sido_gu[1])
        result.append([store_name] + [store_sido_gu1] + [store_address] + [store_phone])
    except:
      break
  return
# CODE 0]

def cswin_Kyochon():
  result = []
  print('Kyochon Address Crawling Start>>>>>>>>>>>>>>>')
  for sido1 in range(1, 18):
    getKyochonAddress(sido1, result)
  kyochon_table = pd.DataFrame(result, columns=('store', 'sido_gungu', 'store_address','store_phone'))
  kyochon_table.to_csv('./kyochon.csv', encoding='utf-8', mode = 'w', index=True)
  del result[:]
  print('finshed')




if __name__ == '__main__':
    cswin_Kyochon()
