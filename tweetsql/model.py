from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from tweetsql.database import Base

tweet_word = Table('tweet_word', Base.metadata,
    Column('tweet_id', Integer, ForeignKey('tweet.id'), nullable=False),
    Column('word_id', Integer, ForeignKey('word.id'), nullable=False))

class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    tweet = Column(String(300), nullable=False)
    tid = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='tweets')
    words = relationship('Word', backref='tweets', secondary=tweet_word)
    created_at = Column(String(100), nullable=False)
    data = Column(Text, nullable=False)

    def __repr__(self):
        return '<Tweet {}>'.format(self.tid)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    screen_name = Column(String(100), nullable=False)
    uid = Column(String(50), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.uid)

class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    word = Column(String(100), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.uid)
