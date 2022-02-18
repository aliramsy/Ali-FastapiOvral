import imp
from fastapi.param_functions import Depends
from jose import JWTError, jwt
from datetime import datetime,timedelta
from typing import Optional
import database,models
from jose.constants import Algorithms
import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from config import settings

oath2_scheme=OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY=settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    
    
    
    try:
        
        payload:str = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        print(e)
        raise credentials_exception  
    
    return token_data
    #at the moment token_data only contain id,but you can add more information to it through auth.py file,for example you can add the level of accessibility via defining role of the user


def get_current_user(token: str= Depends(oath2_scheme),db:Session=Depends(database.get_db)):
    
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)
   
    token=verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user

