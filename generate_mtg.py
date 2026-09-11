import os
import csv
import json
owned_cards = []
from collections import defaultdict

# We'll use a dictionary to track cards so we can build the set indexes in Step 3
sets_data = defaultdict(list)

cards_data = []
with open('cards.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cards_data.append(row)

# --- STEP 1: GENERATE CARDS INTO SET FOLDERS ---
for card in cards_data: # Replace with your actual loop variable
    set_name = card["Set name"]
    card_name = card["Name"]
    # Add the lowercase name to our search inventory list
    owned_cards.append(card_name.lower())
    # Clean the names to prevent slashes from breaking file paths
    safe_set_name = set_name.replace("/", "-").replace(":", "")
    safe_card_name = card_name.replace("/", "-").replace(":", "")
    
    # 1. Create the Set folder dynamically
    folder = f"docs/mtg/{safe_set_name}"
    os.makedirs(folder, exist_ok=True)
    
    # 2. Extract extra details from your CSV
    rarity = card.get("Rarity", "Unknown").capitalize()
    condition = card.get("Condition", "Unknown")
    quantity = card.get("Quantity", "1")
    foil = card.get("Foil", "normal")
    scryfall_id = card.get("Scryfall ID", "")

    # Build the automatic image URL using the Scryfall API
    image_url = f"https://api.scryfall.com/cards/{scryfall_id}?format=image" if scryfall_id else ""
    image_markdown = f"![{card_name}]({image_url})" if scryfall_id else "*No image available*"

    # Create a clean Markdown template for the page
    markdown_content = f"""# {card_name}

{image_markdown}

## Collection Details
| Detail | Value |
|--------|-------|
| **Set** | {set_name} |
| **Rarity** | {rarity} |
| **Condition** | {condition} |
| **Finish** | {foil} |
| **Owned** | {quantity} |
"""

    # Write the card file inside its specific Set folder
    card_path = f"{folder}/{safe_card_name}.md"
    with open(card_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
                
    # 3. Save this card to our tracker for the index page later
    sets_data[safe_set_name].append({
        "name": card_name,
        "filename": f"{safe_card_name}.md"
    })

# --- STEP 3: GENERATE SET INDEX PAGES ---
for safe_set_name, cards in sets_data.items():
    folder = f"docs/mtg/{safe_set_name}"
    index_path = f"{folder}/index.md"
    
    # Write a clean overview page for the set
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"# {safe_set_name}\n\n")
        
        # Sort cards alphabetically so they look nice on the index page
        cards_sorted = sorted(cards, key=lambda x: x["name"])
        for c in cards_sorted:
            f.write(f"* [{c['name']}](./{c['filename']})\n")
# --- STEP 4: GENERATE MAIN MTG GAME PAGE ---

index_content = """# Magic: The Gathering Sets

<div class="grid cards" markdown>
"""

# Loop through our sets alphabetically
for safe_set_name in sorted(sets_data.keys()):
    
    display_name = safe_set_name.replace("-", " ").title()
    
    # Replace spaces with %20 so the markdown link doesn't break
    url_path = safe_set_name.replace(" ", "%20")

    index_content += f"""
- **{display_name}**
  ---
  [Browse Set]({url_path}/index.md)
"""


# Close the HTML grid 
index_content += "\n</div>\n"

# Write the completed string to the main MTG index file
with open("docs/mtg/index.md", "w", encoding="utf-8") as f:
    f.write(index_content)
# --- STEP 5: EXPORT JSON FOR SEARCH TOOL ---
# Save our owned_cards list as a web-friendly JSON file
with open("docs/mtg/inventory.json", "w", encoding="utf-8") as f:
    json.dump(owned_cards, f)
