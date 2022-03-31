from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    SmallInteger,
    String,
    Text,
    Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.engine.row import Row

from app.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    login = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    password = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint('login != ""'),
        CheckConstraint('name != ""'),
        CheckConstraint('password != ""'),
    )

    def __init__(self, login: str, name: str, password: str) -> None:
        self.login = login
        self.name = name
        self.password = password


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)

    reviews_count = Column(Integer, default=0, nullable=False)
    marks_count = Column(Integer, default=0, nullable=False)
    rating = Column(Float, default=0, nullable=False)

    __table_args__ = (
        CheckConstraint('title != ""'),
        CheckConstraint('year > 1900 and year < 2100'),
    )


    def __init__(self, title: str, year: int) -> None:
        self.title = title
        self.year = year


class Review(Base):
    __tablename__ = 'review'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=False)
    text = Column(Text, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'movie_id'),
        CheckConstraint('text != ""'),
    )

    user = relationship('User', lazy='joined')
    movie = relationship('Movie', lazy='joined')

    def __init__(self, user_id: int, movie_id: int, text: str) -> None:
        self.user_id = user_id
        self.movie_id = movie_id
        self.text = text


class Mark(Base):
    __tablename__ = 'mark'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=False)
    score = Column(SmallInteger, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'movie_id'),
        CheckConstraint('score between 0 and 10'),
    )

    user = relationship('User', lazy='joined')
    movie = relationship('Movie', lazy='joined')

    def __init__(self, user_id: int, movie_id: int, score: int) -> None:
        self.user_id = user_id
        self.movie_id = movie_id
        self.score = score
