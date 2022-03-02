from itertools import count
from logging import raiseExceptions
from fastapi import APIRouter,status,HTTPException,Depends
from typing import List,Optional
import schemas,models
from database import engine,get_db
from sqlalchemy.orm import Session
import oath
from sqlalchemy import func

router = APIRouter(
    prefix="/post",
    tags=["posts"]
)

models.Base.metadata.create_all(bind=engine)
#**Post.dict()
@router.post("/",status_code=status.HTTP_201_CREATED)
async def post(request:schemas.Post,db:Session=Depends(get_db),current_user:int=Depends(oath.get_current_user)):
    new_post=models.Post(title=request.title,content=request.content,owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
#you can add search  route to show allpost variable
@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.Ropost])
async def get_all(db:Session=Depends(get_db),current_user:int = Depends(oath.get_current_user),limit:int=10,skip:Optional[int]=0,search:Optional[str]=""):
   #allpost=db.query(models.Post).filter(models.Post.owner_id == current_user.id ).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    likepost=db.query(models.Post,func.count(models.Like.post_id).label("likes")).join(models.Like,models.Post.id== models.Like.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id ).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return likepost

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Ropost)
async def get_post(id,db:Session=Depends(get_db),current_user:int=Depends(oath.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    postlike=db.query(models.Post,func.count(models.Like.post_id).label("likes")).join(models.Like,models.Post.id== models.Like.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the post you are looking for is not found")
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you can not see these posts")
    
    return postlike

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete(id,db:Session=Depends(get_db),current_user:int = Depends(oath.get_current_user)):
    dpost=db.query(models.Post).filter(models.Post.id==id)
    dpost1=dpost.first()
    if not dpost1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="there is no user like this")
    if current_user.id != dpost1.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you are not allowed to delete this post")
    dpost.delete(synchronize_session=False)
    db.commit()
    return "done"

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
async def update(id,request:schemas.Post,db:Session=Depends(get_db),current_user:int = Depends(oath.get_current_user)):
    update_post=db.query(models.Post).filter(models.Post.id==id)
    update_post1=update_post.first()
    if not update_post1:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the post you are looking for is not found")
    if current_user.id != update_post1.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you are not allowed to update this post")
    update_post.update({"content": request.content,"title":request.title},synchronize_session='evaluate')
    db.commit()
    return "updated"
