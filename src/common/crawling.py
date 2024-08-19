import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

def newsCrawling(date, id1, id2):
  dateStr = date.strftime("%Y%m%d")
  baseUrl = f"https://news.naver.com/main/list.naver?mode=LS2D&mid=sec&sid1={id1}&sid2={id2}&date={dateStr}"
  headers = {'User-Agent': 'Mozilla/5.0'}
  
  newsData = []
  previousNewsData = None
  page = 1
  
  while True:
    url = f"{baseUrl}&page={page}"
    print(f'{url} 페이지 크롤링 시작')
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      newsList1 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li')
      newsList2 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li')
      newsList = newsList1 + newsList2
      if not newsList:
        break
      if previousNewsData == newsList:
        break
      previousNewsData = newsList
      for news in newsList:
        try:
          imgElement = news.select_one('dl > dt.photo > a > img')
          if imgElement:
            title = news.select_one('dl > dt:nth-child(2) > a').text.strip()
            url = news.select_one('dl > dt:nth-child(2) > a')['href']
            imgUrl = news.select_one('dl > dt.photo > a > img')['src']
          else:
            title = news.select_one('dl > dt > a').text.strip()
            url = news.select_one('dl > dt > a')['href']
            imgUrl = None
          summary = news.select_one('dl > dd > span.lede').text.strip()
          press = news.select_one('dl > dd > span.writing').text.strip()
          # 기사 본문 링크를 따라가서 본문 가져오기
          articleRes = requests.get(url, headers=headers)
          if articleRes.status_code == 200:
            articleSoup = BeautifulSoup(articleRes.text, 'html.parser')
            content = articleSoup.select_one('#dic_area').text.strip().replace('\u200b', '').replace('\xa0', '').replace('\r', '').replace('\n', '').replace('\t', '')
            date = articleSoup.select_one('#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span').text.strip()
          else:
            content = ''
            date = ''
          newsData.append({'date': convertToTimestamp(date),
                            'title': title,
                            'url': url,
                            'imgUrl': imgUrl,
                            'summary': summary,
                            'content': content,
                            'press' : press
                          })
        except Exception as e:
          print(e);
          continue
    page += 1
  
  return newsData

# 날짜 형식을 변환하는 함수
def convertToTimestamp(dateStr):
    # '오전' 또는 '오후'가 있는지 확인 후 시간 변환
    if '오후' in dateStr:
        dateStr = dateStr.replace('오후', '').strip()
        timeFormat = '%Y.%m.%d. %I:%M'  # %I는 12시간제 포맷
        dt = datetime.strptime(dateStr, timeFormat)
        dt = dt.replace(hour=dt.hour + 12 if dt.hour < 12 else dt.hour)  # 오후이므로 12시간 더함
    elif '오전' in dateStr:
        dateStr = dateStr.replace('오전', '').strip()
        timeFormat = '%Y.%m.%d. %I:%M'
        dt = datetime.strptime(dateStr, timeFormat)
    else:
        # 오후/오전 없이 날짜가 주어졌을 경우 기본적으로 처리
        timeFormat = '%Y.%m.%d. %H:%M'
        dt = datetime.strptime(dateStr, timeFormat)
    return dt
  