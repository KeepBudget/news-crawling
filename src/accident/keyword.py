# -*- coding: utf-8 -*-
from konlpy.tag import Okt
from collections import Counter

okt = Okt()

def addKeywordsToNews(news):
  nouns = okt.nouns(news['content'])
  count = Counter(nouns)
  result = [{word: freq} for word, freq in count.items() if freq > 1]
  news['keywords'] = result
  return news

def addKeywordsToNewsList(newsList):
  newsListWithKeywords = []
  for news in newsList:
    newsWithKeywords = addKeywordsToNews(news)
    if newsWithKeywords['keywords']:
      newsListWithKeywords.append(news)
  return newsListWithKeywords