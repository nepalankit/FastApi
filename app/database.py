from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL=os.getenv('DATABASE_CONNECTION_URI')

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)


Base=declarative_base()

def get_db(): #make a session to the database and close it once we are done
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
    
#connect to database
# while True:
#     try:
#         conn=psycopg2.connect(host=os.getenv('DATABASE_HOST'),database=os.getenv('DATABASE_NAME'),
#                             user=os.getenv('DATABASE_USER'),password=os.getenv('DATABASE_PASSWORD'),cursor_factory=RealDictCursor)
#         cur=conn.cursor()
#         print("Database connection was successful")
#         break

#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error:",error)
#         time.sleep(2)