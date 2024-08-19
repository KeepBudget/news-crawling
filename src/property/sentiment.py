# -*- coding: utf-8 -*-
import os
import tensorflow as tf
from nltk import sent_tokenize
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow_addons as tfa
import numpy as np
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

import nltk
nltk.download('punkt')

MAX_SEQ_LEN = 64

TOKEN_MODEL = "klue/bert-base"
tokenizerModel = BertTokenizer.from_pretrained(TOKEN_MODEL)

baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENTIMENT_MODEL = os.path.join(baseDir, 'model', 'best_model.h5')
sentimentModel = tf.keras.models.load_model(SENTIMENT_MODEL, custom_objects={'TFBertForSequenceClassification': TFBertForSequenceClassification})

def convertData(datas):
  tokens, masks, segments = [], [], []
  for data in datas:
    token = tokenizerModel.encode(data, truncation = True, padding = 'max_length', max_length = MAX_SEQ_LEN)
    numZeros = token.count(0)
    mask = [1] * (MAX_SEQ_LEN - numZeros) + [0] * numZeros
    segment = [0]*MAX_SEQ_LEN
    tokens.append(token)
    masks.append(mask)
    segments.append(segment)
  tokens = np.array(tokens)
  masks = np.array(masks)
  segments = np.array(segments)
  return [tokens, masks, segments]

# 중립 0, 긍정 1 , 부정 2
def convertStatusToLabel(status):
  if status == 0 : return "NEUTRAL"
  elif status == 1 : return "POSITIVE"
  else: return "NEGATIVE"

def sentimentAnalysis(text):
  text = str(text)
  sentenceTokens = sent_tokenize(text)
  input = convertData(sentenceTokens)
  predictedValue = sentimentModel.predict(input) # 예측하기
  predictedStatus = np.argmax(predictedValue, axis=1) # 예측된 라벨(각 문장별로 예측 결과)
  results = [0, 0, 0]
  for status in predictedStatus:
    results[int(status)] += 1
  return {
    "neutral" : round(results[0]/sum(results), 2),
    "positive" : round(results[1]/sum(results), 2),
    "negative" : round(results[2]/sum(results), 2),
  }
  
def addSentimentsToNewsList(newsList):
  for news in newsList:
    sentiments = sentimentAnalysis(news['content'])
    news['sentiments'] = sentiments
  return newsList