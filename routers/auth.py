from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
import schemas,models,oath
from hashing import verify_password
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db,engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/login",response_model=schemas.Token, status_code=status.HTTP_202_ACCEPTED)
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    #oath2 has only username and password object.username performs as username and email
    userlogin=db.query(models.User).filter(models.User.email==request.username).first()
    if not userlogin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="username or password is incorrect")
    if not verify_password(request.password,userlogin.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="username or password is incorrect")
    
    access_token = oath.create_access_token(
        data={"user_id": userlogin.id}
    )

    return {"access_token": access_token, "token_type": "bearer"}
