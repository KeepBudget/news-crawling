import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from district.repository import findDistricts

def getDistrics():
  return findDistricts();

def addDistrictToNews(news, districts):
  # news = {date, title, url, imgUrl, summary, content}
  # districts = [{id, name}, ...]
  news['districts'] = []
  for district in districts:
    if district[1] in news['content']:
      news['districts'].append(district[0])
  return news
      
def addDistrictToNewsList(newsList, districts):
  newsListWithDistricts= []
  for news in newsList:
    newsWithDistrcits = addDistrictToNews(news, districts)
    if newsWithDistrcits['districts']:
      newsListWithDistricts.append(newsWithDistrcits)
  return newsListWithDistricts