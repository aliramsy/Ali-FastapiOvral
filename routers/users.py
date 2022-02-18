from fastapi import APIRouter,status,HTTPException,Depends
import schemas,models
from sqlalchemy.orm import Session
from database import engine,get_db
from hashing import get_password_hash
from typing import List

router=APIRouter(
    prefix="/user",
    tags=["users"]
)
models.Base.metadata.create_all(bind=engine)


@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(request:schemas.User,db:Session=Depends(get_db)):
    hashed_password=get_password_hash(request.password)
    new_user=models.User(username=request.username,email=request.email,password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.Ruser])
async def getalluser(db:Session=Depends(get_db)):
    getuser=db.query(models.User).all()
    
    return getuser

@router.get("/{id}",status_code=status.HTTP_200_OK ,response_model=schemas.Ruser)
async def getuser(id,db:Session=Depends(get_db)):
    userbyid=db.query(models.User).filter(models.User.id==id).first()
    if not userbyid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the user you are looking for is not found")
    return userbyid
