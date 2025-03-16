from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import setup_database, get_session, Winloss, Decklist

def update_winloss(session):
    # Get all decklists first
    decklists = session.query(Decklist).all()
    print(f"Found {len(decklists)} decklists")
    print("Enter 'q' to quit, 'p' to pause, or press Enter to skip a player")

    for decklist in decklists:
        # Check if winloss record exists with values
        winloss = session.query(Winloss).filter_by(decklist_id=decklist.id).first()
        
        if winloss and winloss.wins is not None and winloss.losses is not None:
            print(f"\nSkipping {decklist.playername} - already has records (W: {winloss.wins}, L: {winloss.losses})")
            continue

        print(f"\nPlayer: {decklist.playername}")
        
        if not winloss:
            winloss = Winloss(decklist_id=decklist.id)
            session.add(winloss)
        
        try:    
            wins = input(f"Enter wins for {decklist.playername} (current: {winloss.wins}): ")
            if wins.lower() == 'q':
                print("\nSaving and quitting...")
                session.commit()
                return
            elif wins.lower() == 'p':
                print(f"\nPaused at player: {decklist.playername}")
                session.commit()
                return
            elif wins.strip():  # Only update if input is not empty
                winloss.wins = int(wins)
            
            losses = input(f"Enter losses for {decklist.playername} (current: {winloss.losses}): ")
            if losses.lower() == 'q':
                print("\nSaving and quitting...")
                session.commit()
                return
            elif losses.lower() == 'p':
                print(f"\nPaused at player: {decklist.playername}")
                session.commit()
                return
            elif losses.strip():  # Only update if input is not empty
                winloss.losses = int(losses)
            
            session.commit()
            print(f"Updated record - Wins: {winloss.wins}, Losses: {winloss.losses}")
            
        except ValueError:
            print("Invalid input! Please enter numbers only.")
            session.rollback()
        except KeyboardInterrupt:
            print("\nSaving progress and exiting...")
            session.commit()
            return

if __name__ == "__main__":
    print("Starting win/loss update process...")
    print("Commands:")
    print("  - Enter number to update wins/losses")
    print("  - Press Enter to skip")
    print("  - Enter 'q' to quit")
    print("  - Enter 'p' to pause")
    engine = setup_database()
    session = get_session(engine)
    update_winloss(session)
    print("Win/loss update completed.")