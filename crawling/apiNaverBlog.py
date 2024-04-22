import os
import sys
import urllib.request
import datetime
import time
import json
import ssl

client_id = 'RRyWQVOaR7eiDHUsJNmA'
client_secret = 'jK2XXVdVFp'

#[CODE 1]
def getRequestUrl(url): #API 요청 URL을 호출하여 응답을 받아오는 함수
    req = urllib.request.Request(url) #url 요청
    req.add_header("X-Naver-Client-Id", client_id) #헤더에 client_id 추가
    req.add_header("X-Naver-Client-Secret", client_secret) #헤더에 client_secret 추가

    # SSL 인증서 검증 무시(맥북만)
    context = ssl._create_unverified_context()

    try:
        response = urllib.request.urlopen(req,context=context) #요청한 url을 열어서 response에 저장
        if response.getcode() == 200: #요청이 성공했을 경우
            print("[%s] Url Request Success" % datetime.datetime.now()) #성공 메시지 출력
            return response.read().decode('utf-8') #요청한 url의 내용을 반환
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url)) #에러 메시지 출력
        return None

#[CODE 2]
def getNaverSearch(node, srcText, start, display): #네이버 검색 API를 호출하는 함수
    base = "https://openapi.naver.com/v1/search" #네이버 검색 API 호출을 위한 기본 URL
    node = "/%s.json" % node #검색할 대상을 node에 추가
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display) #검색어, 검색 시작 위치, 검색 결과 출력 건수를 parameters에 추가

    url = base + node + parameters #url에 base, node, parameters를 추가
    responseDecode = getRequestUrl(url) #[CODE 1] #url을 호출하여 응답을 받아옴

    if (responseDecode == None): #응답이 없을 경우
        return None
    else:
        return json.loads(responseDecode) #json 형태로 반환

#[CODE 3]
def getPostData(post, jsonResult, cnt): #검색 결과 중 원하는 데이터를 추출하는 함수
    title = post['title'] #검색 결과 중 title을 title에 저장
    description = post['description'] #검색 결과 중 description을 description에 저장
    link = post['link'] #검색 결과 중 link를 link에 저장
    bloggername = post['bloggername'] #차이점1.#검색 결과 중 bloggername을 bloggername에 저장
    pDate = datetime.datetime.strptime(post['postdate'], '%Y%m%d') #검색 결과 중 postdate를 pDate에 저장
    pDate = pDate.strftime('%Y-%m-%d') #pDate의 형식을 'YYYY-MM-DD'로 변환
    # 포스트 날짜를 가져와서 포맷 변경


    jsonResult.append({'cnt': cnt, 'title': title, 'description': description, #jsonResult에 cnt, title, description, link, bloggername, pDate를 추가
                       'link': link, 'bloggername': bloggername, 'postdate': pDate,})
    return

#[CODE 0]
def main():
    node = 'blog' #크롤링할 대상
    srcText = input('검색어를 입력하세요: ') #검색어 입력
    cnt = 0 #검색 결과 건수를 저장할 변수
    jsonResult = [] #검색 결과를 저장할 리스트

    jsonResponse = getNaverSearch(node, srcText, 1, 100) #[CODE 2] #네이버 검색 API를 호출하여 검색 결과를 jsonResponse에 저장
    if jsonResponse is not None: #검색 결과가 있는 경우
        total = jsonResponse['total'] #검색 결과 중 total을 total에 저장
    else:
        print("API 요청에 실패했습니다.") #API 요청에 실패했을 경우
        return

    while ((jsonResponse != None) and (jsonResponse['display'] != 0)): #검색 결과가 있는 경우
        for post in jsonResponse['items']: #검색 결과 중 items를 post에 저장
            cnt += 1 #검색 결과 건수를 1 증가
            getPostData(post, jsonResult, cnt) #[CODE 3] #검색 결과 중 원하는 데이터를 추출하여 jsonResult에 저장
        start = jsonResponse['start'] + jsonResponse['display'] #검색 시작 위치를 start에 저장
        jsonResponse = getNaverSearch(node, srcText, start, 100) #[CODE 2] #다음 검색 결과를 호출하여 jsonResponse에 저장
    print('전체 검색 : %d 건' %total) #전체 검색 건수 출력

    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile: #검색어와 node를 파일명으로 하는 json 파일을 생성
        jsonFile = json.dumps(jsonResult, indent = 4, sort_keys = True, ensure_ascii = False) #json 형태로 변환
        outfile.write(jsonFile) #json 파일로 저장
    print("가져온 데이터 : %d 건" %(cnt)) #가져온 데이터 건수 출력
    print('%s_naver_%s.json SAVED' % (srcText, node)) #저장 완료 메시지 출력
    # 블로그 검색 결과 출력
    for result in jsonResult: #jsonResult를 result에 저장
        print(result['title']) #검색 결과 중 title 출력
        print(result['description']) #검색 결과 중 description 출력
        print(result['link']) #검색 결과 중 link 출력
        print()
if __name__ == '__main__':
    main()