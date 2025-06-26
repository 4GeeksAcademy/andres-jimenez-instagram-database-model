from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(120))
    profile_picture: Mapped[str] = mapped_column(String(200))
    bio: Mapped[str] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    followers: Mapped[int] = mapped_column(Integer, default=0)

    posts = relationship("Post", back_populates="user")
    stories = relationship("Story", back_populates="user")
    comments = relationship("Comment", back_populates="author")
    followers_rel = relationship(
        "Follower", foreign_keys="[Follower.user_to_id]", back_populates="followed")
    following_rel = relationship(
        "Follower", foreign_keys="[Follower.user_from_id]", back_populates="follower")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
            # do not serialize the password
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'))
    caption: Mapped[str] = mapped_column(String(2200))
    likes: Mapped[int] = mapped_column(Integer, default=0)
    saves: Mapped[int] = mapped_column(Integer, default=0)

    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post")
    comments = relationship("Comment", back_populates="post")


class Story(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'))
    available: Mapped[bool] = mapped_column(Boolean(), default=True)

    user = relationship("User", back_populates="stories")


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(db.ForeignKey('post.id'))
    author_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'))
    text: Mapped[str] = mapped_column(String(1000))

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(db.ForeignKey('post.id'))
    file_type: Mapped[str] = mapped_column(String(20))
    url: Mapped[str] = mapped_column(String(500))

    post = relationship("Post", back_populates="media")


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'))
    user_to_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'))

    follower = relationship("User", foreign_keys=[
                            user_from_id], back_populates="following_rel")
    followed = relationship("User", foreign_keys=[
                            user_to_id], back_populates="followers_rel")
