from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(8), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    following: Mapped[List["Follower"]] = relationship(back_populates="from_user", foreign_keys="Follower.user_from_id",)
    followers: Mapped[List["Follower"]] = relationship(back_populates="to_user", foreign_keys="Follower.user_to_id",)
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(120), nullable=False)
    img_url: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[List["Media"]] = relationship(back_populates="post")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")



    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "img_url": self.img_url,
            "user_id": self.user_id,
            # do not serialize the password, its a security breach
        }

class Comment(db.Model):

    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "post_id": self.post_id,
            "author_id": self. author_id,
            # do not serialize the password, its a security breach
        }
    
class Media(db.Model):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(120), nullable=False)
    url: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="media")
    
  

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "type": self.type,
            "post_id": self.post_id,
            # do not serialize the password, its a security breach
        }
    
class Follower(db.Model):
    __tablename__ = "follower"
    id: Mapped[int] = mapped_column(primary_key=True)
	
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    from_user: Mapped["User"] = relationship(back_populates="following", foreign_keys=[user_from_id])
    to_user: Mapped["User"] = relationship(back_populates="followers", foreign_keys=[user_to_id])
    

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
            # do not serialize the password, its a security breach
        }