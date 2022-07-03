from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas, utils 
from ..database import get_db

#good practice to use routers to split up the code
router = APIRouter(
    prefix="/users", #optional, less typing good practice for complex FastAPI
    tags=['Users'] #groups them
)

#adding a new user (UserOut removes the password field)
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) #by default send a 201 status code 
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #create the hash of the password and update the password with the hashed version 
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user