from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String , Boolean
from sqlalchemy.sql.expression import text 
from sqlalchemy.orm import relationship
from .database import Base 

#everytime you make a change to the model you have to drop the table first
#sqlalchemymodel
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key = True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    #no impact in the database, but gives us information on the user (figures out the relationship) 
    #sqlalchemy will do this 
    owner = relationship("User")

#New ORM model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key = True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
