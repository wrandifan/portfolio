import os
import requests
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import db
from db import setup_database, get_session, Decklist, Deck, Card

def fetch_card_info(card):
    response = requests.get(f"https://api.scryfall.com/cards/named?exact={card.cardname}")
    if response.status_code == 200:
        card_data = response.json()
        card.cmc = card_data.get('cmc')
        card.mana_cost = card_data.get('mana_cost')
        card.color_identity = ','.join(card_data.get('color_identity', []))
        card.type_line = card_data.get('type_line')
        print(f"Fetched data for card: {card.cardname}")
    else:
        print(f"Error fetching data for card: {card.cardname}, Status Code: {response.status_code}")

def import_decklists(session, folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r') as file:
                lines = file.readlines()
                playername = filename.replace('.txt', '')
                new_decklist = Decklist(playername=playername)
                session.add(new_decklist)
                session.commit()

                main_or_side = "main"
                for line in lines:
                    line = line.strip()
                    if not line:
                        main_or_side = "side"
                        continue
                    parts = line.split()
                    if len(parts) < 2:
                        print(f"Skipping invalid line in {filename}: {line}")
                        continue
                    try:
                        quantity = int(parts[0])
                    except ValueError:
                        print(f"Skipping invalid quantity in {filename}: {line}")
                        continue
                    cardname = ' '.join(parts[1:])
                    
                    # Check if the card already exists in the Card table
                    card = session.query(Card).filter_by(cardname=cardname).first()
                    if not card:
                        card = Card(cardname=cardname)
                        fetch_card_info(card)
                        session.add(card)
                        session.commit()
                    
                    deck_card = Deck(decklist_id=new_decklist.id, card_id=card.id, cardname=cardname, quantity=quantity, main_or_side=main_or_side)
                    session.add(deck_card)
                session.commit()

if __name__ == "__main__":
    engine = setup_database()
    session = get_session(engine)
    import_decklists(session, 'd:/Aetherdrift Pro Tour Analysis/decklists')