import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def connectDB():
  return pymysql.connect(
    host=os.environ.get("FLASK_DB_HOST"),
    port=int(os.environ.get("FLASK_DB_PORT")),
    user=os.environ.get("FLASK_DB_USER"),
    password=os.environ.get("FLASK_DB_PASSWORD"),
    db=os.environ.get("FLASK_DB_NAME"),
    charset='utf8'
  )