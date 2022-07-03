from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings

#provide the endpoint of our login - no slash 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET KEY -> verifies data integrity -resides on our server 
#Algorithm
#Expiration Time of the token 
#have to provide a string (from docs) - will turn into env variables later 
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    #adding the expiration time (must be utc)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

#returns nothing when successful
def verify_access_token(token: str, credentials_exception):
    
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        #notice before we passed user_id to the token
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        
        #make sure all the information is there thats listed in the schema
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

#pass this as a dependency in our path operations - it will take the token from the request automatically, verify the token is correct, extract the id, and fetch the user from db 
#and add it to our path operation function 
def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token =  verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
