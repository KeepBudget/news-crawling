# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.crawling import newsCrawling
from district.service import getDistrics, addDistrictToNewsList
from property.sentiment import addSentimentsToNewsList
from property.repository import saveNews

def savedPropertyNews(date, dateStr):
  # id1 = 101(경제) & id2 = 260(부동산)
  crawledNews = newsCrawling(date, 101, 260)
  numCrawledNews = len(crawledNews)
  print(f'{dateStr}의 뉴스 {numCrawledNews}개 크롤링 완료')
  districts = getDistrics()
  newsWithDistricts = addDistrictToNewsList(crawledNews, districts)
  numNewsWithDistricts = len(newsWithDistricts)
  print(f'{dateStr}의 뉴스 {numNewsWithDistricts}개 지역 추가 완료')
  newsWithSentiments = addSentimentsToNewsList(newsWithDistricts)
  numNewsWithSentiments = len(newsWithSentiments)
  print(f'{dateStr}의 뉴스 {numNewsWithSentiments}개 감정 분석 결과 추가 완료')
  for news in newsWithSentiments:
    saveNews(news)