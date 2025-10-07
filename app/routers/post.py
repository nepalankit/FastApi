from fastapi import FastAPI,status,HTTPException,Response,Depends,APIRouter
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
from ..import models,utils
from ..database import engine,get_db
from ..schemas import Post,PostCreate
from fastapi.security import OAuth2PasswordRequestForm
from .. import oauth2

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('/',response_model=List[Post])
async def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cur.execute(""" SELECT * FROM posts""")
    # posts=cur.fetchall()
        #  SEE ONLY YOUR POSTS. posts= db.query(models.Post).filter(models.Post.owner_id==current_user.id).all() #.all() runs sql query
        posts=db.query(models.Post).all()
        return posts


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=Post )
def create_posts(post:PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cur.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post=cur.fetchone()
    # conn.commit()
    
   
    # new_post=models.Post(title=post.title,content=post.content,published=post.published)
     #convereting this line to dictionary is really handy.Does the same thing as above
    #
    print("Incoming post data:", post)
    print("Current user:", current_user.id)

    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # just like returning *
    return new_post





#single posts
# def find_post(id):
#     for p in my_posts:
#         if p['id']==id:
#             return p

@router.get('/{id}',response_model=Post)
def get_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
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

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cur.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id),))
    # deleted_post=cur.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
    
    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
@router.put('/{id}',response_model=PostCreate)
def update_post(id:int,updated_post:PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cur.execute("""UPDATE posts SET title=%s,content=%s,published=%s where id=%s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post=cur.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
        
    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()