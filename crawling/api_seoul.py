import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd


#[CODE 1]
def getRequestUrl(url):    #API 요청 URL을 호출하여 응답을 받아오는 함수
    req = urllib.request.Request(url)     #url 요청
    try: 
        response = urllib.request.urlopen(req) #요청한 url을 열어서 response에 저장
        if response.getcode() == 200: #요청이 성공했을 경우
            print ("[%s] Url Request Success" % datetime.datetime.now()) #성공 메시지 출력
            return response.read().decode('utf-8') #요청한 url의 내용을 반환
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url)) #에러 메시지 출력
        return None

#[CODE 2]
def getPage(st): #서울시 자유제안 목록을 가져오는 함수
    service_url = "http://openAPI.seoul.go.kr:8088/7a4c6f6a786e79753932565763426d/json/ChunmanFreeSuggestions/{}/{}".format(st,st+4) #서비스 URL

    url = service_url
    print(url)  # 액세스 거부 여부 확인용 출력
    retData = getRequestUrl(url) #[CODE 1] #url을 호출하여 응답을 받아옴

    if (retData == None): #응답이 없을 경우
        return None
    else:
        return json.loads(retData) #json 형태로 반환

#[CODE 3]
def getItemAll(): #서울시 자유제안 목록을 가져오는 함수
    jsonResult = [] #결과를 저장할 리스트
    result = [] #결과를 저장할 리스트
    for i in range(200): #200페이지까지 반복
        jsonData = getPage(i*5 + 1) #페이지별로 5개씩 가져옴
        if jsonData['ChunmanFreeSuggestions']['RESULT']['CODE'] == 'INFO-000': #데이터가 있는 경우

            for item in range(5): #5개의 데이터를 가져옴
                sn = jsonData['ChunmanFreeSuggestions']['row'][item]['SN'] #제안번호
                title = jsonData['ChunmanFreeSuggestions']['row'][item]['TITLE'] #제안제목
                content = jsonData['ChunmanFreeSuggestions']['row'][item]['CONTENT'] #제안내용
                vote_score = jsonData['ChunmanFreeSuggestions']['row'][item]['VOTE_SCORE'] #득표
                reg_date = jsonData['ChunmanFreeSuggestions']['row'][item]['REG_DATE'] #제안등록일자

                print('제안번호: {}, 제안제목: {}, 득표: {}, 제안등록일자: {}'.format(sn, title, vote_score, reg_date)) #출력

                jsonResult.append({'제안번호': sn, '제안제목': title, '제안내용': content, '득표': vote_score, '제안등록일자': reg_date}) #jsonResult에 추가

                result.append([sn, title, content, vote_score, reg_date]) #result에 추가

        if jsonData['ChunmanFreeSuggestions']['RESULT']['CODE'] == 'INFO-100': #데이터가 없는 경우
            print("인증키 유효 x") #인증키 유효하지 않음
            return

    print('총 건수 : %s' %jsonData['ChunmanFreeSuggestions']['list_total_count']) #총 건수 출력
    return jsonResult, result #jsonResult, result 반환

#[CODE 0]
def main(): #메인 함수
    jsonResult,result = getItemAll()#[CODE 3] #서울시 자유제안 목록을 가져옴

    print("<< 수집합니다. >>")

    #파일저장 1 : json 파일
    with open('./seoul.csv','w', encoding = 'utf8') as outfile: #json 파일을 생성
        jsonFile = json.dumps(jsonResult, indent = 4, sort_keys = True, ensure_ascii = False) #json 형태로 변환
        outfile.write(jsonFile) #json 파일로 저장
    #파일저장 2 : csv 파일
    columns = ["제안번호", "제안제목", "제안내용", "득표", "제안등록일자"] #컬럼명
    result_df = pd.DataFrame(result, columns = columns) #데이터프레임 생성
    result_df.to_csv('./seoul.csv', index=False, encoding='utf-8-sig') #csv 파일로 저장

if __name__ == '__main__':
    main()
