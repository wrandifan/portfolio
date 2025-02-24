import os
import csv

# Folder containing decklist text files
INPUT_FOLDER = "decklists"
OUTPUT_FILE = "decklists.csv"

def parse_decklist(file_path):
    """Parses a decklist file into structured data."""
    deck_name = os.path.splitext(os.path.basename(file_path))[0]
    data = []
    section = "Mainboard"  # Default section

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                if section == "Mainboard":
                    section = "Sideboard"
                continue  # Skip empty lines

            parts = line.split(" ", 1)
            if len(parts) == 2:
                quantity, card_name = parts
                data.append([deck_name, card_name, int(quantity), section])

    return data

def process_decklists():
    """Reads all decklist files and writes to a CSV."""
    all_data = []

    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".txt"):  # Process only text files
            file_path = os.path.join(INPUT_FOLDER, filename)
            all_data.extend(parse_decklist(file_path))

    # Write to CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Deck Name", "Card Name", "Quantity", "Type"])  # Header
        writer.writerows(all_data)

    print(f"CSV file created: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_decklists()
