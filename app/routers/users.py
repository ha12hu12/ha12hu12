from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import user_create_data_schema, user_create_out_schema, user_get_out_schema
from app import models, utils 

router = APIRouter(tags=['Users'])
@router.post("/users/create_user", response_model=user_create_out_schema, status_code=status.HTTP_201_CREATED)
def create_user(data: user_create_data_schema, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"there is already a user with email: {data.email}")
        
    data.password = utils.hash_password(data.password)
    new_user = models.User(**data.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user

@router.get("/users/get_user/{id}", response_model=user_get_out_schema)
def get_user(id:int, db:Session = Depends(get_db)):
    the_user =  db.query(models.User).filter(models.User.id == id).first()

    if not the_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no user with the id: {id}")

    return the_user