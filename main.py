from fastapi import FastAPI


app=FastAPI()

@app.get('/') #decorator makes api endpoint
async def root():
    return {"message":"hello world"}

@app.get('/posts')

async def get_posts():
    return {'data:"your posts"}'}