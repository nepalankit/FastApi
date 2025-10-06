from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone
from . import schemas
from fastapi import Depends, status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")


#secret key

#Algorithm

#expiration time
SECRET_KEY = os.getenv('DATABASE_SECRET_KEY')
ALGORITHM = os.getenv('DATABASE_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('DATABASE_ACCESS_TOKEN_EXPIRE_MINUTES')

def create_access_token(data: dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
        
        
        
    except JWTError:
        raise credentials_exception
    
    return token_data
    
    
    
def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    
    return verify_access_token(token,credentials_exception)