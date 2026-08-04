from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import post_get_schema, post_create_out_schema, post_create_data_schema
from app import models, oauth2

router = APIRouter(tags=["Posts"])

#get exact one post
@router.get("/posts/get_post/{id}", response_model=post_get_schema)
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    the_post = db.query(models.Post).filter(models.Post.id == id)
    if not the_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no post with id: {id}")

    return the_post.first()

#get all posts
@router.get("/posts", response_model=post_get_schema)
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).first()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no posts in the database")

    return posts

#create post
@router.post('/posts/create_post', response_model=post_create_out_schema, status_code=status.HTTP_201_CREATED)
def create_post(data: post_create_data_schema, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    data_dict = data.dict()
    data_dict["owner_id"] = current_user.id
    print(data)
    new_post = models.Post(**data_dict)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post 

@router.put('/posts/update_post/{id}')
def update_post(id: int, updated_post: post_create_data_schema, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    the_post = get_post(id=id)

    the_post.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    db.refresh(the_post)
    return the_post

@router.delete("/posts/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    the_post = get_post(id = id)

    the_post.delete(synchronize_session = False)
    db.commit()

    return "seccfully"

    