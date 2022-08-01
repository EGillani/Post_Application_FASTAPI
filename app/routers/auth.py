from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login',summary="Access and refresh tokens for user (does not automatically grant access to other endpoints in /docs)", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    
    #the OAuth2PasswordRequestForm will return the username and password (no email etc., but username will be our email) 
    #whatever the user sends will be stored in the username
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #have to verify the passwords are equal
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    #create a token 
    #return token
    access_token = oauth2.create_access_token(data= {"user_id": user.id})

    return {"access_token" : access_token, "token_type": "bearer"}