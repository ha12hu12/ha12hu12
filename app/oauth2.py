from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .schemas import data_to_encode_schema, token_info
from  .database import get_db
from .config import settings
from app import models
oauth2 = OAuth2PasswordBearer(tokenUrl='login')
# we  need 3 things to make JWT tokens:
# secret_key
# algorithm
# expire time 
secret_key = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_minutes = settings.access_token_expire_minutes
def create_access_token(data: data_to_encode_schema):
    data_copy = data.copy()
    exp_time = datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_minutes)
    data_copy["exp"] =  exp_time
    access_token = jwt.encode(data_copy, secret_key, algorithm=ALGORITHM)

    return access_token

def veryfie_access_token(token):
    try:
        decoded_token = jwt.decode(token=token, key=secret_key, algorithms=[ALGORITHM])
        the_id  = decoded_token.get("id")
        if not the_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong id <:")

        token_data = token_info(id=the_id)
        return token_data
    except  JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you didnt login  or you need to re-login bc token has expired")
    
def get_current_user(token = Depends(oauth2), db: Session = Depends(get_db)):
    token = veryfie_access_token(token=token)
    the_user = db.query(models.User).filter(models.User.id == token.id).first()
    return the_user

