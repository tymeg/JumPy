'''
Module with sqlalchemy database table and functions concerning game's scoreboard
'''

import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select, delete
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from typing import List

base = declarative_base()
engine = create_engine('sqlite:///' + os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "scoreboard.sqlite"), echo=True)


class Scoreboard(base):
    '''
    Scoreboard reprents a database table with top 10 scores

    Attributes:
        id (Column[int]): score's ID
        nick (Column[Text]): nick of score's gainer
        score (Column[int]): score 
    '''
    __tablename__ = 'scoreboard'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nick = Column(String, nullable=False)
    score = Column(Integer, nullable=False)

base.metadata.create_all(engine)

def is_good_enough_score(score: int) -> bool:
    '''
    Tells if score is in top 10

    Args:
        score (int): player's final score

    Returns:
        bool: True if score is in top 10, False otherwise
    '''
    Session = sessionmaker(bind=engine)
    session = Session()

    scores_ascending = session.execute(select(Scoreboard).order_by(
        Scoreboard.score)).scalars().all()

    return len(scores_ascending) < 10 or score > scores_ascending[0].score


def add_score(score: int, nick: str) -> None:
    '''
    Adds score to scoreboard database table

    Args:
        score (int): score to add
        nick (str): score gainer's nick
    '''
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


def get_scoreboard() -> List[Scoreboard]:
    '''
    Gets a list of top 10 scores

    Returns:
        List[Scoreboard]: list of Scoreboard's table rows
    '''
    Session = sessionmaker(bind=engine)
    session = Session()

    scoreboard = session.execute(select(Scoreboard).order_by(
        Scoreboard.score)).scalars().all()[::-1]
    return scoreboard
