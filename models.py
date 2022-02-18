from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base
from sqlalchemy.orm import relationship

#String(50)
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True , nullable= False)
    title = Column(String, index=True ,nullable=False)
    content = Column(String, index=True ,nullable=False)
    published = Column(Boolean, server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    owner=relationship("User")
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,unique=True, primary_key=True, index=True , nullable= False)
    email=Column(String,unique=True, index=True ,nullable=False)
    username=Column( String,unique=True ,index=True,nullable=False )
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    password=Column(String,nullable=False)


class Like(Base):
    __tablename__ = "likes"

    post_id=Column(Integer,  ForeignKey("posts.id", ondelete="CASCADE"),nullable=False, primary_key=True )
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)

