from sqlalchemy import  Column, Integer, VARCHAR, BOOLEAN , TIMESTAMP, String, ForeignKey, PrimaryKeyConstraint
from  sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key = True)
    title = Column(VARCHAR(100), nullable = False)
    content = Column(VARCHAR(500), nullable =  False)
    published =  Column(BOOLEAN,  server_default = text("True"))
    created_at = Column(TIMESTAMP(timezone=True), server_default = text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable  = False)

    owner = relationship("User")

    
class User(Base):
    __tablename__ = "users"
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    id = Column(Integer, primary_key = True)
    created_at = Column(TIMESTAMP(timezone=True), server_default = text('now()'))

class Votes(Base):
    __tablename__ = "votes"

    Post_id = Column(Integer, ForeignKey(column="posts.id", ondelete="CASCADE") )
    User_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE") )

    __table_args__ = (
        PrimaryKeyConstraint('Post_id', 'User_id'),
    )