import csv
import os
import re

def slugify(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    name = name.strip('-')
    return name

# Scryfall image URL builder
def scryfall_image_url(scryfall_id):
    return f"https://api.scryfall.com/cards/{scryfall_id}?format=image&version=png"

# Rarity icon mapping
RARITY_ICONS = {
    "common": "⬤",
    "uncommon": "◆",
    "rare": "★",
    "mythic": "✶"
}

generated_cards = []

# OPEN YOUR CSV
with open('cards.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]

    for row in reader:
        name = row['name']
        set_code = row['set code']
        set_name = row['set name']
        collector = row['collector number']
        rarity = row['rarity'].lower()
        quantity = row['quantity']
        condition = row['condition']
        finish = row['foil']
        language = row['language']
        scryfall_id = row['scryfall id']

        game = "mtg"
        folder = f"docs/{game}"
        os.makedirs(folder, exist_ok=True)

        # MkDocs‑safe filename
        safe_name = slugify(name)

        filename = f"{folder}/{safe_name}.md"
        generated_cards.append((safe_name, name))

        rarity_icon = RARITY_ICONS.get(rarity, "⬤")
        image_url = scryfall_image_url(scryfall_id)

        tags = [
            f"rarity:{rarity}",
            f"set:{set_code}",
            f"condition:{condition}",
            f"finish:{finish}",
            f"lang:{language}",
            f"collector:{collector}"
        ]

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {name}\n\n")
            f.write(f"**Set:** {set_name} ({set_code})\n\n")
            f.write(f"**Collector Number:** {collector}\n\n")
            f.write(f"**Rarity:** {rarity_icon} {rarity.title()}\n\n")
            f.write(f"**Condition:** {condition}\n\n")
            f.write(f"**Finish:** {finish}\n\n")
            f.write(f"**Language:** {language}\n\n")
            f.write(f"**Game:** Magic: The Gathering\n\n")
            f.write(f"![Card Image]({image_url})\n\n")
            f.write("**Tags:**\n\n")
            for tag in tags:
                f.write(f"- {tag}\n")

# Build index page
index_path = "docs/mtg/index.md"
with open(index_path, 'w', encoding='utf-8') as index:
    index.write("# All Magic: The Gathering Cards\n\n")
    index.write("Browse all MTG cards in the Vault18 catalog.\n\n")

    for safe_name, display_name in sorted(generated_cards, key=lambda x: x[1]):
        index.write(f"- [{display_name}]({safe_name}.md)\n")
