from flask import Flask
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

from src.property.service import savedPropertyNews
from src.accident.service import saveAccidentNews

def getPreviousDateNews():
  currentDate = datetime.now()
  previousDate = currentDate - timedelta(days=1)
  previousDateStr = previousDate.strftime("%Y년 %m월 %d일")
  print(f'{previousDateStr}의 뉴스 크롤링 시작')
  savedPropertyNews(previousDate, previousDateStr)
  saveAccidentNews(previousDate, previousDateStr)
  print(f'{previousDateStr}의 뉴스 저장 완료')
  
scheduler = BackgroundScheduler()
scheduler.add_job(getPreviousDateNews, 'cron', hour=2, minute=0)
scheduler.start()

if __name__=="__main__":
  app.run();