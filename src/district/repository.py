import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.mysql import connectDB

def findDistricts():
  try:
    db = connectDB();
    cursor = db.cursor()
    sql = "select * from districts"
    cursor.execute(sql)
    distrcits = cursor.fetchall()
    cursor.close()
    db.close()
    return distrcits
  except:
    print("지역 가져오기 오류")