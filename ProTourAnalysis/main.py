import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sqlite3
import sqlalchemy

dbfile = "sqlite:///aetherdrift.db"
con = sqlite3.connect("aetherdrift.db")
cur = con.cursor()

# Query to find which players have extra cards in their decklist
query = """
SELECT decklist.playername, decklist.id, SUM(deck.quantity) as mainboard_count
FROM deck
JOIN decklist ON deck.decklist_id = decklist.id
WHERE deck.main_or_side = 'main'
GROUP BY decklist.id
HAVING mainboard_count > 60
"""
cur.execute(query)
df = pd.DataFrame(cur.fetchall(), columns=[i[0] for i in cur.description])
print(df)
print("Number of players with more than 60 cards in their mainboard: ", len(df))

# Query to categorize decks by color identity
query = """
SELECT decklist.playername, decklist.id, GROUP_CONCAT(DISTINCT card.color_identity) as color_identities
FROM deck
JOIN decklist ON deck.decklist_id = decklist.id
JOIN card ON deck.card_id = card.id
WHERE deck.main_or_side = 'main'
GROUP BY decklist.id
"""
cur.execute(query)
color_identity_df = pd.DataFrame(cur.fetchall(), columns=[i[0] for i in cur.description])
print(color_identity_df)

# Function to combine color identities
def combine_color_identities(color_identities):
    combined = set()
    for ci in color_identities.split(','):
        combined.update(ci)
    return ''.join(sorted(combined))

# Apply the function to combine color identities for each deck
color_identity_df['combined_color_identity'] = color_identity_df['color_identities'].apply(combine_color_identities)
print(color_identity_df[['playername', 'combined_color_identity']])

# Plot the most prevalent color identities by decks
plt.figure(figsize=(12, 8))
sns.countplot(x='combined_color_identity', data=color_identity_df, order=color_identity_df['combined_color_identity'].value_counts().index)
plt.title('Most Prevalent Color Identities by Decks')
plt.xlabel('Combined Color Identity')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# Plot the most prevalent color identities by players


#query to find highest winrate
query = """
SELECT decklist.playername, winloss.wins, winloss.losses, 
       (winloss.wins * 1.0 / (winloss.wins + winloss.losses)) as winrate
FROM winloss
JOIN decklist ON winloss.decklist_id = decklist.id
ORDER BY winrate DESC"""
cur.execute(query)
winrate_df = pd.DataFrame(cur.fetchall(), columns=[i[0] for i in cur.description])
print(winrate_df)
print("Highest winrate: ", winrate_df.loc[winrate_df['winrate'].idxmax()])

#analyze winrate by color identity
