from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas, utils , oauth2
from ..database import get_db
from sqlalchemy.exc import  SQLAlchemyError, IntegrityError
from sqlalchemy import func
from typing import List
import logging 

logger = logging.getLogger(__name__)

#good practice to use routers to split up the code
router = APIRouter(
    prefix="/users", #optional, less typing good practice for complex FastAPI
    tags=['Users'] #groups them
)

#adding a new user (UserOut removes the password field)
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) #by default send a 201 status code 
#don't use query parameters it will show in the url path!
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #create the hash of the password and update the password with the hashed version 
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    try: 
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:
        logger.error(e)
        db.rollback()
        raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                             detail="Integrity error! Please make sure the username is not already registered in this application!")
    except SQLAlchemyError as e:
        logger.error(e)
        db.rollback()
        raise  HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, 
                             detail="SqlAlchemyError! Reach out to developer and sorry for the inconvenience!")
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                             detail=f"Oh no, something went horribly wrong, you can let the developer know! They are sorry!")
    return new_user

@router.get('', response_model=schemas.UserOut)
def get_user(username: str,  db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.username == username).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                             detail=f"Oh no, something went horribly wrong, you can let the developer know! They are sorry!")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user


@router.get('/{id}/posts', response_model=List[schemas.PostOut])
def get_user_posts(id: int,  db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)):
            
    #making sure the user is only viewing their own posts 
    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action. Please sign in as user: {id} to view all your posts.")
    
    try:
        posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).where(models.Post.owner_id == id).group_by(models.Post.id).all()
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                             detail=f"Oh no, something went horribly wrong, you can let the developer know! They are sorry!")

    
    return posts