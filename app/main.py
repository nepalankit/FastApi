from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
from .import models
from .database import engine
from .routers import post, user, auth,like
from fastapi.middleware.cors import CORSMiddleware

from alembic import command
from alembic.config import Config

#hasing algorithm
pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')


#we have alembic now we dont need this to generate tables.
# models.Base.metadata.create_all(bind=engine)
load_dotenv()


app=FastAPI()
origins=["*"] #allow all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #allow all origins
    allow_credentials=True,
    allow_methods=["*"], #allow all methods
    allow_headers=["*"], #allow all headers
)


@app.on_event("startup")
def run_migrations():
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print(" Migrations applied.")
    except Exception as e:
        print(f"Migration error: {e}")
# Include routers
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(like.router)

@app.get('/') #decorator makes api endpoint
async def root():
    return {"message":"hello world"}

# @app.get('/sqlalchemy')
# def test_posts(db:Session=Depends(get_db)):
#         posts= db.query(models.Post).all() #.all() runs sql query
#         return {"data":posts}


