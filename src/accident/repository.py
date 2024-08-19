import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.mysql import connectDB

def saveNews(news):
  # news - date, title, url, imgUrl, summary, content, press, districts, sentiments
  try:
    db = connectDB()
    cursor = db.cursor()
    
    # 뉴스 저장
    sqlSaveNews  = """
    INSERT INTO news (title, summary, press, date, img_url, origin_url)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sqlSaveNews, (news['title'], news['summary'], news['press'], news['date'], news['imgUrl'], news['url']))
    newsId = cursor.lastrowid
    
    # 뉴스 distrcits 저장
    sqlSaveNewsDistricts = """
    INSERT INTO news_districts (news_id, district_id, category)
    VALUES (%s, %s, 'ACCIDENT')
    """
    for districtId in news['districts']:
      cursor.execute(sqlSaveNewsDistricts, (newsId, districtId))
    
    # 뉴스 Sentiments 저장
    sqlSaveNewskeywords = """
    INSERT INTO news_keywords (news_id, keyword, count)
    VALUES (%s, %s, %s)
    """
    keywordItems = news['keywords']
    for keywordItem in keywordItems:
      for keyword, count in keywordItem.items():
        cursor.execute(sqlSaveNewskeywords, (newsId, keyword, count))
    
    db.commit()
    cursor.close()
    db.close()
  except Exception as e:
    print(e)