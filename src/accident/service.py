# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.crawling import newsCrawling
from district.service import getDistrics, addDistrictToNewsList
from accident.keyword import addKeywordsToNewsList
from accident.repository import saveNews

def saveAccidentNews(date, dateStr):
  # id1 = 102(사회) & id2 = 249(사건사고)
  crawledNews = newsCrawling(date, 102, 249)
  numCrawledNews = len(crawledNews)
  print(f'{dateStr}의 뉴스 {numCrawledNews}개 크롤링 완료')
  districts = getDistrics()
  newsWithDistricts = addDistrictToNewsList(crawledNews, districts)
  numNewsWithDistricts = len(newsWithDistricts)
  print(f'{dateStr}의 뉴스 {numNewsWithDistricts}개 지역 추가 완료')
  newsWithKeywords = addKeywordsToNewsList(newsWithDistricts)
  numNewsWithKeywords = len(newsWithKeywords)
  print(f'{dateStr}의 뉴스 {numNewsWithKeywords}개 키워드 추가 완료')
  for news in newsWithKeywords:
    saveNews(news)