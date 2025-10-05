from .. import models,schemas,utils
from fastapi import FastAPI,status,HTTPException,Response,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from .. import schemas,models,utils




router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

#create users



@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    #hash the password - user.password
    
        
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#getusers
@router.get('/')
def get_users(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users

#get user by id
@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} does not exist")
    
    return user