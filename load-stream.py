#!/usr/bin/env python

import json
import twitter
from tweetsql.database import Base, db_session, engine
from tweetsql.model import Hashtag, Tweet, User, Word
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

CONSUMER_KEY = 'secret'
CONSUMER_SECRET = 'secret'

OAUTH_TOKEN = 'secret'
OAUTH_TOKEN_SECRET = 'secret'

TRACK = 'water'

twitter_auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_stream = twitter.TwitterStream(auth=twitter_auth)

statuses = twitter_stream.statuses.filter(track=TRACK)

for t in statuses:
    print(t['text'])
    try:
        u = db_session.query(User).filter_by(uid=str(t['user']['id'])).one()
    except NoResultFound:
        u = User(screen_name=t['user']['screen_name'], uid=t['user']['id'])
        db_session.add(u)
        db_session.commit()

    tw = Tweet(tweet=t['text'], tid=t['id'], user_id=u.id, created_at=t['created_at'], data=json.dumps(t))

    try:
        words = tw.tweet.split()
        for w in words:
            try:
                w_obj = db_session.query(Word).filter(Word.word == w).one()
            except MultipleResultsFound:
                pass
            except NoResultFound:
                w_obj = Word(word=w)
                db_session.add(w_obj)
                db_session.commit()
                tw.words.append(w_obj)
        db_session.add(tw)
        db_session.commit()
    except OperationalError:
        db_session.rollback()
