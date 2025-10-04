from fastapi import FastAPI,status,HTTPException,Response,Depends
from fastapi import Body
from pydantic import BaseModel
from typing import Optional, Dict, List
from random import randrange
from sqlalchemy.orm import Session
import psycopg2
import time
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from .import models
from .database import engine,get_db
from .schemas import PostBase,Post,PostCreate,UserCreate,UserOut

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
    
    

my_posts=[{"title":"title of post 1", "content":"content of post 1","id":1},
          {"title":"title of post 2", "content":"content of post 2","id":2}]

@app.get('/') #decorator makes api endpoint
async def root():
    return {"message":"hello world"}

# @app.get('/sqlalchemy')
# def test_posts(db:Session=Depends(get_db)):
#         posts= db.query(models.Post).all() #.all() runs sql query
#         return {"data":posts}


@app.get('/posts',response_model=List[Post])
async def get_posts(db:Session=Depends(get_db)):
    # cur.execute(""" SELECT * FROM posts""")
    # posts=cur.fetchall()
        posts= db.query(models.Post).all() #.all() runs sql query
        return posts


@app.post('/posts',status_code=status.HTTP_201_CREATED,response_model=Post )
def create_posts(post:PostCreate,db:Session=Depends(get_db)):
    # cur.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post=cur.fetchone()
    # conn.commit()
    
   
    # new_post=models.Post(title=post.title,content=post.content,published=post.published)
     #convereting this line to dictionary is really handy.Does the same thing as above
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # just like returning *
    return new_post





#single posts
# def find_post(id):
#     for p in my_posts:
#         if p['id']==id:
#             return p

@app.get('/posts/{id}',response_model=Post)
def get_post(id:int,db:Session=Depends(get_db)):
    # cur.execute(""" SELECT * FROM posts where id=%s""",(str(id),))
    # single_post=cur.fetchone()
    # print(single_post)
    single_post=db.query(models.Post).filter(models.Post.id==id).first()
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")


    return single_post


#delete post

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id']==id:
#             return i

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    # cur.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id),))
    # deleted_post=cur.fetchone()
    # conn.commit()
    posts=db.query(models.Post).filter(models.Post.id==id)
    
    if posts.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
    posts.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
@app.put('/posts/{id}',response_model=PostCreate)
def update_post(id:int,updated_post:PostCreate,db:Session=Depends(get_db)):
    # cur.execute("""UPDATE posts SET title=%s,content=%s,published=%s where id=%s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post=cur.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)

    if post_query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()


@app.post('/users',status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
