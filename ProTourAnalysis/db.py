import os
import requests
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Decklist(Base):
    __tablename__ = 'decklist'
    id = Column(Integer, primary_key=True)
    playername = Column(String)
    cards = relationship("Deck", back_populates="decklist")
    winloss = relationship("Winloss", back_populates="decklist")

class Winloss(Base):
    __tablename__ = 'winloss'
    id = Column(Integer, primary_key=True)
    decklist_id = Column(Integer, ForeignKey('decklist.id'))
    wins = Column(Integer)
    losses = Column(Integer)
    decklist = relationship("Decklist", back_populates="winloss")    

class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    cardname = Column(String, unique=True)
    cmc = Column(Integer)
    mana_cost = Column(String)
    color_identity = Column(String)
    type_line = Column(String)
    decks = relationship("Deck", back_populates="card")

class Deck(Base):
    __tablename__ = 'deck'
    id = Column(Integer, primary_key=True)
    decklist_id = Column(Integer, ForeignKey('decklist.id'))
    card_id = Column(Integer, ForeignKey('card.id'))
    cardname = Column(String)  # Removed unique=True constraint
    quantity = Column(Integer)
    main_or_side = Column(String)
    decklist = relationship("Decklist", back_populates="cards")
    card = relationship("Card", back_populates="decks")

def setup_database():
    engine = create_engine('sqlite:///aetherdrift.db')
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()