from fastapi import FastAPI,status,HTTPException,Response,Depends
from fastapi import Body
from typing import Optional, Dict, List
from random import randrange
from sqlalchemy.orm import Session
import psycopg2
import time
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from .import models,utils
from .database import engine,get_db

from .routers import post,user








models.Base.metadata.create_all(bind=engine)
load_dotenv()


app=FastAPI()



    
    
#connect to database
while True:
    try:
        conn=psycopg2.connect(host=os.getenv('DATABASE_HOST'),database=os.getenv('DATABASE_NAME'),
                            user=os.getenv('DATABASE_USER'),password=os.getenv('DATABASE_PASSWORD'),cursor_factory=RealDictCursor)
        cur=conn.cursor()
        print("Database connection was successful")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error:",error)
        time.sleep(2)
    
    
app.include_router(post.router)
app.include_router(user.router)



@app.get('/') #decorator makes api endpoint
async def root():
    return {"message":"hello world"}

# @app.get('/sqlalchemy')
# def test_posts(db:Session=Depends(get_db)):
#         posts= db.query(models.Post).all() #.all() runs sql query
#         return {"data":posts}




