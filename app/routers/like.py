from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2,database


router=APIRouter(
    prefix="/like",
    tags=['Like']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def like_post(like:schemas.Like,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    
        post=db.query(models.Post).filter(models.Post.id==like.post_id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {like.post_id} does not exist")
                   
        like_query=db.query(models.Like).filter(models.Like.post_id==like.post_id,models.Like.user_id==current_user.id)
        found_like=like_query.first()
    
    
        if (like.dir==1):
            if found_like:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already liked post {like.post_id}")
            
            new_like=models.Like(post_id=like.post_id,user_id=current_user.id)
            db.add(new_like)
            db.commit()
            return {"message":"successfully liked post"}
        
        else:
            if not found_like: #we cannot delete something that does not exist
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="like does not exist"
                                    )
                
            like_query.delete(synchronize_session=False) #synchronize sesssion is used  performance optimization
            db.commit()
            return {"message":"successfully deleted like"}
                
                
        
        
        