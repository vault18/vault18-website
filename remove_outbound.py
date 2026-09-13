import csv

# File names
master_file = 'cards.csv'
outbound_file = 'outbound.csv'

# 1. Load the outbound cards into a dictionary for easy lookup
outbound_cards = {}
with open(outbound_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Create a unique key using Name and Set (adjust column names to match your CSV)
        key = (row['Name'], row['Set name']) 
        outbound_cards[key] = int(row['Quantity'])

# 2. Process the master inventory
updated_inventory = []
with open(master_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        key = (row['Name'], row['Set name'])
        
        # If the card is in the outbound list, reduce its quantity
        if key in outbound_cards:
            current_qty = int(row['Quantity'])
            remove_qty = outbound_cards[key]
            new_qty = current_qty - remove_qty
            
            row['Quantity'] = str(new_qty)
            
        # Only keep the card if the quantity is greater than 0
        if int(row['Quantity']) > 0:
            updated_inventory.append(row)

# 3. Overwrite the master file with the updated inventory
with open(master_file, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_inventory)

print("Inventory updated successfully!")
