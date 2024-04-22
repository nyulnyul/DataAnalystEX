import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd

#출입국관광통계서비스 일반 인증키(Encoding)
ServiceKey = "7a4c6f6a786e79753932565763426d"

#[CODE 1]
def getRequestUrl(url):    #API 요청 URL을 호출하여 응답을 받아오는 함수
    req = urllib.request.Request(url)     #url 요청
    try: 
        response = urllib.request.urlopen(req) #요청한 url을 열어서 응답 데이터를 response에 저장
        if response.getcode() == 200: #요청이 성공했을 경우
            print ("[%s] Url Request Success" % datetime.datetime.now()) #성공 메시지 출력
            return response.read().decode('utf-8') #요청한 url의 내용을 반환
    except Exception as e: #요청이 실패했을 경우
        print(e) #에러 메시지 출력
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url)) #에러 메시지 출력
        return None

#[CODE 2]
def getTourismStatsItem(yyyymm, national_code, ed_cd): #입국자 통계를 가져오는 함수
    service_url = "http://openAPI.seoul.go.kr:8088/7a4c6f6a786e79753932565763426d/xml/ChunmanFreeSuggestions/1/5" #서비스 URL

    parameters = "?_type=json&serviceKey=" + ServiceKey #인증키 #파라미터 추가
    parameters += "&YM=" + yyyymm #기준연월
    parameters += "&NAT_CD=" + national_code #국가코드
    parameters += "&ED_CD=" + ed_cd #외래객 체류자격코드

    url = service_url + parameters #요청할 url
    print(url)   #액세스 거부 여부 확인용 출력 #실제로는 주석처리
    retData = getRequestUrl(url) #[CODE 1] #url을 호출하여 응답을 받아와 객체에 저장

    if (retData == None): #응답이 없을 경우
        return None
    else:
        return json.loads(retData) #json 형태로 반환

#[CODE 3]
def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear): #입국자 통계를 가져오는 함수
    jsonResult = [] #결과를 저장할 리스트
    result = [] #결과를 저장할 리스트
    natName = '' #natName 변수에 기본값 설정
    ed = ''  # ed 변수에 기본값 설정
    dataEND = "{0}{1:0>2}".format(str(nEndYear), str(12)) #수집할 데이터의 끝 날짜인 dataEND를 nEndYear의 12월로 설정
    isDataEnd = 0 #수집한 데이터의 끝인지 확인하기 위한 플래그인 IsDataEnd를 0으로 설정
    for year in range(nStartYear, nEndYear+1): #입력한 연도 범위만큼 반복
        for month in range(1, 13): #1월부터 12월까지 반복
            if(isDataEnd == 1): break #데이터 마지막 항목인 경우 반복문 종료
            yyyymm = "{0}{1:0>2}".format(str(year), str(month)) #수집할 연도와 월을 여섯 자리로 맞추어 yyyymm에 저장
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd) #[CODE 2] #getTourismStatsItem()을 호출해 받은 월 데이터를 jsonData에 저장
            if (jsonData['response']['header']['resultMsg'] == 'OK'): #데이터가 있는 경우
                #데이터가 없는 마지막 항목인 경우 ----------------------------
                if jsonData['response']['body']['items'] == '':
            #['items'] 항목에 값이 없으면 출입국관광통계 데이터가 아직 들어가지 않은 마지막 월이므로 날짜를 dataEND에 저장하고 데이터 수집 작업을 중단
                    isDataEnd = 1  #데이터 마지막 항목인지 확인
                    dataEND = "{0}{1:0>2}".format(str(year), str(month-1)) #데이터 마지막 항목을 저장
                    print("데이터 없음.... \n제공되는 통계 데이터는 %s년 %s월까지입니다." %(str(year), str(month-1))) #데이터가 없는 경우 메시지 출력
                    break
                #jsonData를 출력하여 확인 ----------------------------
                print(json.dumps(jsonData, indent = 4, sort_keys = True, ensure_ascii = False)) #수집한 데이터 json 형태로 출력
                natName = jsonData['response']['body']['items']['item']['natKorNm'] #국가명
                natName = natName.replace(' ', '') #공백 제거
                num = jsonData['response']['body']['items']['item']['num'] #입국자 수
                ed = jsonData['response']['body']['items']['item']['ed'] #외래객 체류자격 코드
                print('[ %s_%s : %s ]' %(natName, yyyymm, num)) #입력한 국가명, 기준연월, 입국자 수 출력
                print('-----------------------------------------------------')
                jsonResult.append({'nat_name': natName, 'nat_cd': nat_cd, 'yyyymm': yyyymm, 'visit_cnt': num}) #jsonResult에 nat_name, nat_cd, yyyymm, visit_cnt 추가
                result.append([natName, nat_cd, yyyymm, num]) #result에 natName, nat_cd, yyyymm, num 추가
    return (jsonResult, result, natName, ed, dataEND) #jsonResult, result, natName, ed, dataEND 반환

#[CODE 0]
def main(): #메인 함수
    jsonResult = [] #결과를 저장할 리스트
    result = [] #결과를 저장할 리스트

    print("<< 국내 입국한 외국인의 통계 데이터를 수집합니다. >>") #프로그램 시작 메시지 출력
    nat_cd = input('국가 코드를 입력하세요(중국: 112 / 일본: 130 / 미국: 275) : ') #국가 코드 입력
    nStartYear = int(input('데이터를 몇 년부터 수집할까요? : ')) #데이터 수집 시작 연도 입력
    nEndYear = int(input('데이터를 몇 년까지 수집할까요? : ')) #데이터 수집 종료 연도 입력
    ed_cd = "E" #E : 방한외래관광객, D : 해외 출국 #외래객 체류자격 코드
    jsonResult, result, natName, ed, dataEND = getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear) #[CODE 3] #함수통해 반환받은 데이터를 각각에 저장

    #파일저장 1 : json 파일
    with open('./%s_%s_%d_%s.json' % (natName, ed, nStartYear, dataEND),'w', encoding = 'utf8') as outfile: #파일명을 국가명, 외래객 체류자격 코드, 시작연도, 데이터마지막연월로 저장
        jsonFile = json.dumps(jsonResult, indent = 4, sort_keys = True, ensure_ascii = False) #json 형태로 변환
        outfile.write(jsonFile) #json 파일로 저장
    #파일저장 2 : csv 파일
    columns = ["입국자국가", "국가코드", "입국연월", "입국자 수"] #데이터 프레임을 만들 컬럼명
    result_df = pd.DataFrame(result, columns = columns) #데이터 프레임 객체 생성
    result_df.to_csv('./%s_%s_%d_%s.csv' % (natName, ed, nStartYear, dataEND), index=False, encoding='cp949') #객체를 csv 파일로 저장

if __name__ == '__main__': #메인 함수 호출
    main()
