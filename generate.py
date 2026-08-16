import csv, os

with open('cards.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        game = row['game'].lower()
        name = row['name'].replace('/', '-')
        filename = f"docs/{game}/{name}.md"
        image_path = f"../images/{game}/{row['image']}"

        with open(filename, 'w', encoding='utf-8') as md:
            md.write(f"# {row['name']}\n\n")
            md.write(f"**Set:** {row['set']}\n\n")
            md.write(f"**Number:** {row['number']}\n\n")
            md.write(f"![Card Image]({image_path})\n")
