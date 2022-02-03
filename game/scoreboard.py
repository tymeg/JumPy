import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select, delete
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()
engine = create_engine('sqlite:///' + os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "scoreboard.sqlite"), echo=True)
base.metadata.create_all(engine)


class Scoreboard(base):
    __tablename__ = 'scoreboard'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nick = Column(String, nullable=False)
    score = Column(Integer, nullable=False)


def is_good_enough_score(score):
    Session = sessionmaker(bind=engine)
    session = Session()

    scores_ascending = session.execute(select(Scoreboard).order_by(
        Scoreboard.score)).scalars().all()

    return len(scores_ascending) < 10 or score > scores_ascending[0].score


def add_score(score, nick):
    Session = sessionmaker(bind=engine)
    session = Session()

    scores_before = session.execute(select(Scoreboard)).scalars().all()
    session.add(Scoreboard(nick=nick, score=score))
    session.commit()

    # delete last score(s)
    if len(scores_before) == 10:
        last_score_id = session.execute(select(Scoreboard).order_by(
            Scoreboard.score)).scalars().all()[0].id
        session.execute(delete(Scoreboard).where(
            Scoreboard.id == last_score_id))
        session.commit()


def get_scoreboard():
    Session = sessionmaker(bind=engine)
    session = Session()

    scoreboard = session.execute(select(Scoreboard).order_by(
        Scoreboard.score)).scalars().all()[::-1]
    return scoreboard
