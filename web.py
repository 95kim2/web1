from bs4 import BeautifulSoup
from selenium import webdriver

def makeURL(_url, _stn, _yy, _obs, _x='14', _y='2'):
    URL = _url + '?' + 'stn=' + _stn +'&yy=' + _yy + '&obs=' + _obs + '&x=' + _x + '&y=' + _y
    return URL

#서울108 인천112 수원119 청주131 대전133 광주156 대구143
#포항138 울산152 부산159 창원155
cities = ["seoul", "incheon", "suwon", "cheongju", "daejeon", "gwangju", "daegu"\
          ,"pohang", "ulsan", "busan", "changwon"]
cities_num = ["108", "112", "119", "131", "133", "156", "143", "138", "152", "159", "155"]
url = 'https://www.weather.go.kr/weather/climate/past_table.jsp'
yy = ["2020", "2019", "2018"]
obs = ["07", "10", "08", "21", "06", "12", "35", "59"]
obs_str = ["평균기온", "최저기온", "최고기온", "강수량", "평균풍속", "상대습도", "일조시간", "운량"]
# 07평균기온 10최저기온 08최고기온 21강수량
# 06평균풍속 12상대습도 35일조시간 59운량

# 기본 url과 원하는 페이지의 변수들을 넣어서 원하는 정보 스크래핑하는 함수
def fileWriteWeather(city, stn, url, yy, obs, obs_str, x="14", y="2"):
    f = open('./'+city+'.txt', 'w')
    f.write('날짜 ')
    for ii in range(len(obs)):
        f.write(obs_str[ii])
        f.write(' ')
    f.write('\n')

    # 원하는 연도만큼 반복
    for idx_yy in range(len(yy)):
        # 1월~12월까지 저장할 딕셔너리 구조 틀 만들
        dict_weather = {}
        for i in range(12):
            key_month = str(i+1)+'월'
            dict_weather[key_month] = {}
            for j in range(31):
                key_day = str(j+1)+'일'
                dict_weather[key_month][key_day] = []

        # 크롬드라이버로 해당 url 열어서 원하는 부분 긁어오기 -> 딕셔너리 형태로 1월~12월까지 저장
        for idx in range(len(obs)):
            driver = webdriver.Chrome('./chromedriver')
            print(idx)
            url_weather = makeURL(url, stn, yy[idx_yy], obs[idx])
            print(url_weather)
            driver.get(url_weather)
            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')

            weathers = soup.select('#content_weather > table > tbody > tr > td')
            cnt = 1
            num = 12*31
            for weather in weathers:
                if (num == 0):
                    break
                if (weather.text.find('일') != -1):
                    key_day = weather.text
                    continue
                key_month = str(cnt) + '월'
                dict_weather[key_month][key_day].append(weather.text)
                cnt += 1
                num -= 1
                if (cnt == 13):
                    cnt = 1
            driver.quit()

        print(dict_weather)

        #파일에 1월부터 12월까지 평균기온, 최저/고기온, 강수량, 풍속, 습도, 일조량, 운량을 기록
        for i in range(12):
            key_month = str(i+1)+'월'
            for j in range(31):
                key_day = str(j+1)+'일'
                if (len(str(i+1)) == 1):
                    month = '0'+str(i+1)
                else:
                    month = str(i+1)
                if (len(str(j+1)) == 1):
                    day = '0'+str(j+1)
                else:
                    day = str(j+1)
                f.write(yy[idx_yy]+'-'+month+'-'+day+' ')
                for data in dict_weather[key_month][key_day]:
                    if data == '\xa0' or data == '':
                        f.write('- ')
                    else:
                        f.write(data+' ')
                f.write('\n')
    f.close()


for i in range(11):
    fileWriteWeather(cities[i], cities_num[i], url, yy, obs, obs_str)