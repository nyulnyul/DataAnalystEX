import os
import sys
import urllib.request
import datetime
import time
import json

client_id = 'RRyWQVOaR7eiDHUsJNmA' # 개발자센터에서 발급받은 Client ID 값
client_secret = 'jK2XXVdVFp' # 개발자센터에서 발급받은 Client Secret 값

#[CODE 1]
def getRequestUrl(url):    #API 요청 URL을 호출하여 응답을 받아오는 함수
    req = urllib.request.Request(url)  #url 요청을 보낼 객체 생성
    req.add_header("X-Naver-Client-Id", client_id) #헤더에 client_id 추가
    req.add_header("X-Naver-Client-Secret", client_secret) #헤더에 client_secret 추가
    
    try:  #예외처리
        response = urllib.request.urlopen(req) #요청한 객체를 보내고 응답을 response에 저장
        if response.getcode() == 200: #요청이 성공했을 경우
            print ("[%s] Url Request Success" % datetime.datetime.now()) #성공 메시지 출력
            return response.read().decode('utf-8') #요청한 url의 내용을 반환
    except Exception as e: #요청이 실패했을 경우
        print(e) #에러 메시지 출력
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url)) #에러 메시지 출력
        return None #아무것도 반환하지 않음

#[CODE 2]
def getNaverSearch(node, srcText, start, display):    #네이버 검색 API를 호출하는 함수
    base = "https://openapi.naver.com/v1/search" #네이버 검색 API 호출을 위한 기본 URL
    node = "/%s.json" % node #검색할 대상을 node에 추가
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display) #검색어, 검색 시작 위치, 검색 결과 출력 건수를 parameters에 추가
    
    url = base + node + parameters    #url에 base, node, parameters를 추가
    responseDecode = getRequestUrl(url)   #[CODE 1] #url을 호출하여 응답을 받아옴
    
    if (responseDecode == None): #응답이 없을 경우
        return None #아무것도 반환하지 않음
    else: #응답이 있을 경우
        return json.loads(responseDecode) #json 형태로 반환

#[CODE 3]
def getPostData(post, jsonResult, cnt):  #검색 결과 중 원하는 데이터를 추출하는 함수
    title = post['title'] #검색 결과 중 title을 title에 저장
    description = post['description'] #검색 결과 중 description을 description에 저장
    org_link = post['originallink'] #검색 결과 중 originallink를 org_link에 저장
    link = post['link'] #검색 결과 중 link를 link에 저장

    pDate = datetime.datetime.strptime(post['pubDate'],'%a, %d %b %Y %H:%M:%S +0900') #검색 결과 중 pubDate를 pDate에 저장
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S') #pDate의 형식을 'YYYY-MM-DD HH:MM:SS'로 변환

    jsonResult.append({'cnt':cnt, 'title':title, 'description': description, #jsonResult에 cnt, title, description, org_link, link, pDate를 추가
                            'org_link':org_link, 'link': org_link, 'pDate':pDate})
    return

#[CODE 0]
def main(): #메인 함수
    node = 'news'   # 크롤링 할 대상 : news
    srcText = input('검색어를 입력하세요: ') #검색어를 입력받음
    cnt = 0 #검색 결과 건수를 저장할 변수
    jsonResult = [] #검색 결과를 저장할 리스트

    jsonResponse = getNaverSearch(node, srcText, 1, 100)  #[CODE 2]
    # getNaverSearch() 함수를 호출하여 start = 1, display= 100에 대한 검색 결과를 반환받아 jsonResponse에 저장
    if jsonResponse is not None: #jsonResponse가 비어있지 않을 경우
        total = jsonResponse['total'] #검색 결과 중 total을 total에 저장
        # 나머지 코드 계속...
    else:
        print("API 요청에 실패했습니다.") #API 요청에 실패했을 경우
        return

    while ((jsonResponse != None) and (jsonResponse['display'] != 0)): #jsonResponse가 비어있지 않고 display가 0이 아닐 경우 = 데이터가 있는동안
        for post in jsonResponse['items']: #검색결과 하나씩 처리 작업 반복 jsonResponse의 items를 post에 저장
            cnt += 1 #검색 결과 건수를 1 증가
            getPostData(post, jsonResult, cnt)  #[CODE 3] #검색 결과 중 원하는 데이터를 추출하여 jsonResult에 저장
        
        start = jsonResponse['start'] + jsonResponse['display'] #반복이 끝나면 검색 시작 위치를 start위치 변경
        # print('cnt %d start %d desplay %d' %(cnt, jsonResponse['start'], jsonResponse['display']))
        jsonResponse = getNaverSearch(node, srcText, start, 100)  #[CODE 2]  #새 검색 결과를 호출하여 jsonResponse에 저장 후 다시 반복
       
    print('전체 검색 : %d 건' %total)
    
    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile: #검색어와 node를 파일명으로 하는 json 파일을 생성
        jsonFile = json.dumps(jsonResult,  indent=4, sort_keys=True,  ensure_ascii=False) #json 형태로 변환
                        
        outfile.write(jsonFile) #json 파일로 저장
        
    print("가져온 데이터 : %d 건" %(cnt)) #가져온 데이터 건수 출력
    print ('%s_naver_%s.json SAVED' % (srcText, node)) #저장 완료 메시지 출력
    
if __name__ == '__main__': #메인 함수 호출
    main() #메인 함수 호출

