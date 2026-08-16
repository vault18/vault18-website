import csv
import os

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

# Store card filenames for index page
generated_cards = []

with open('cards.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        name = row['Card Name']
        set_name = row['Set Name']
        number = row['Collector Number']
        rarity = row['Rarity'].lower()
        condition = row['Condition']
        finish = row['Finish']
        language = row['Language']
        scryfall_id = row['Scryfall ID']

        game = "mtg"

        folder = f"docs/{game}"
        os.makedirs(folder, exist_ok=True)

        # Fix illegal filename characters
        safe_name = (
            name.replace("/", "-")
                .replace("\\", "-")
                .replace(":", "-")
                .replace("*", "-")
                .replace("?", "")
                .replace("\"", "")
                .replace("<", "")
                .replace(">", "")
                .replace("|", "")
        )

        filename = f"{folder}/{safe_name}.md"
        generated_cards.append((safe_name, name))

        rarity_icon = RARITY_ICONS.get(rarity, "⬤")
        image_url = scryfall_image_url(scryfall_id)

        tags = [
            f"rarity:{rarity}",
            f"set:{set_name}",
            f"condition:{condition}",
            f"finish:{finish}",
            f"lang:{language}",
            f"collector:{number}"
        ]

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {name}\n\n")
            f.write(f"**Set:** {set_name}\n\n")
            f.write(f"**Collector Number:** {number}\n\n")
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

    # Sort alphabetically
    for safe_name, display_name in sorted(generated_cards, key=lambda x: x[1]):
        index.write(f"- [{display_name}]({safe_name}.md)\n")
