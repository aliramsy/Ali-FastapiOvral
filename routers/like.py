from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
import schemas,database,oath,models


router = APIRouter(
    prefix="/like",
    tags=["likes"]
)


@router.post("/",status_code=status.HTTP_201_CREATED)
async def like(request:schemas.Like,db:Session=Depends(database.get_db),current_user:int=Depends(oath.get_current_user)):
    postforlike=db.query(models.Post).filter(models.Post.id==request.post_id).first()
    if not postforlike:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="there is no post with id you are looking for")
    likequery=db.query(models.Like).filter(models.Like.post_id==request.post_id,models.Like.user_id==current_user.id)
    likefound=likequery.first()
    if request.dir == 1:
        if likefound:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="you have liked this post before")
        new_like=models.Like(post_id=request.post_id,user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return "{message}:{like successfully added}"
    else:
        if not likefound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="there is no like found")
        else:
            likequery.delete(synchronize_session=False)
            db.commit()
            return "{message}:{the like successfully removed}"
        



