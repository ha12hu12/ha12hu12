from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import user_login_schema
from app import models, utils , oauth2


router = APIRouter(tags=["Authentication"])

@router.post('/users/user_login')
def user_login(data: user_login_schema, db: Session = Depends(get_db)):
    the_user = db.query(models.User).filter(models.User.email == data.email).first()

    if not the_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no user with the email: {data.email}")

    verify_password = utils.verify(plain_password=data.password, hashed_password=the_user.password)    

    if not verify_password:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"WRONG PASSWORD, please try again")
    
    return {"access_token": oauth2.create_access_token(data={"id": the_user.id}), "token_type": "Bearer"}