from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import vote_data_schema
from app import models, oauth2



router  =  APIRouter(tags=['Votes'])


@router.post("/vote")
def vote(data: vote_data_schema, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    the_post =  db.query(models.Post).filter(models.Post.id == data.post_id).first()

    if not the_post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no post with the id: {data.post_id}")

    #def check if aleardy voted
    def check_if_vote_exist():
        vote_query = db.query(models.Votes).filter(models.Votes.Post_id == data.post_id,
                                                   models.Votes.User_id == current_user.id)
        if vote_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                                  detail=f"user with the email: {current_user.email} already liked post with the id: {data.post_id}")
    
    #if dir = true or false
    if  data.dir == True:
        check_if_vote_exist()

        new_vote = models.Votes(Post_id = data.post_id,
                                User_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return f"vote added to: {the_post}"
    else:
            vote= db.query(models.Votes).filter(models.Votes.Post_id == data.post_id,
                                                models.Votes.User_id == current_user.id).first()

            if not vote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"you didnt vote to the post with id {data.post_id}")

            db.delete(vote)
            db.commit()

            return 'seccuffly deleted inshallah'

