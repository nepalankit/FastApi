from fastapi import FastAPI,status,HTTPException,Response,Depends
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from sqlalchemy.orm import Session
import psycopg2
import time
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from .import models
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)
load_dotenv()


app=FastAPI()



class Post(BaseModel):
    title:str
    content:str
    published:bool=True #default value
    
    
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
    
    

my_posts=[{"title":"title of post 1", "content":"content of post 1","id":1},
          {"title":"title of post 2", "content":"content of post 2","id":2}]

@app.get('/') #decorator makes api endpoint
async def root():
    return {"message":"hello world"}

@app.get('/sqlalchemy')
def test_posts(db:Session=Depends(get_db)):
        return db.query(models.Post).all()


@app.get('/posts')
async def get_posts():
    cur.execute(""" SELECT * FROM posts""")
    posts=cur.fetchall()
    print (posts)
    return {'data':posts}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cur.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    new_post=cur.fetchone()
    conn.commit()
    
    return{"data":new_post}





#single posts
def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

@app.get('/posts/{id}')
def get_post(id:int):
    cur.execute(""" SELECT * FROM posts where id=%s""",(str(id),))
    single_post=cur.fetchone()
    print(single_post)
    
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
       
        
    return{"post_detail":single_post}
    

#delete post

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i

@app.delete('/posts/{id}')
def delete_post(id:int,status_code=status.HTTP_204_NO_CONTENT):
    cur.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id),))
    deleted_post=cur.fetchone()
    conn.commit()
    
    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
@app.put('/posts/{id}')
def update_post(id:int,post:Post):
    cur.execute("""UPDATE posts SET title=%s,content=%s,published=%s where id=%s RETURNING * """,(post.title,post.content,post.published,str(id)))
    updated_post=cur.fetchone()
    conn.commit()

    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")

    return {'data':updated_post}