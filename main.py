from fastapi import FastAPI,status,HTTPException
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True #default value
    rating:Optional[int]=None #optional value
    

my_posts=[{"title":"title of post 1", "content":"content of post 1","id":1},
          {"title":"title of post 2", "content":"content of post 2","id":2}]

@app.get('/') #decorator makes api endpoint
async def root():
    return {"message":"hello world"}

@app.get('/posts')
async def get_posts():
    return {'data':my_posts}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    
    return{"data":post_dict}





#single posts
def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

@app.get('/posts/{id}')
def get_post(id:int):
    
    post=find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
       
        
    return{"post_detail":post}
    
    