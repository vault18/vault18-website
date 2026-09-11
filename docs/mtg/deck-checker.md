Paste your decklist below (one card per line) to check it against the Vault18 inventory. 

<textarea id="deckInput" rows="12" style="width: 100%; padding: 10px; background-color: #1e1e1e; color: #fff; border: 1px solid #333; border-radius: 5px; font-family: monospace;" placeholder="Example: 1 Sol Ring..."></textarea>

<button id="checkBtn" onclick="checkDeck()" style="margin-top: 15px; padding: 10px 20px; background-color: #aa00ff; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">Check Vault Inventory</button>

<div class="grid cards" markdown>

-   **✅ In Stock**

    <ul id="inStockList" style="color: #4caf50; list-style-type: none; padding: 0;"></ul>

-   **❌ Missing**

    <ul id="missingList" style="color: #f44336; list-style-type: none; padding: 0;"></ul>

</div>

<script>
async function checkDeck() {
    const btn = document.getElementById('checkBtn');
    btn.innerText = "Checking Vault18...";
    btn.style.opacity = "0.6";
    btn.disabled = true;

    await new Promise(resolve => setTimeout(resolve, 500));

    const response = await fetch('../inventory.json');
    
    if (!response.ok) {
        alert("Error loading inventory! Check the F12 Console.");
        btn.innerText = "Check Vault Inventory";
        btn.style.opacity = "1";
        btn.disabled = false;
        return;
    }

    const inventory = await response.json(); 
    
    const rawText = document.getElementById('deckInput').value;
    const lines = rawText.split('\n');
    
    let inStock = [];
    let missing = [];
    
    lines.forEach(line => {
        let cardName = line.trim();
        if (!cardName) return; 
        
        cardName = cardName.replace(/^\d+\s*x?\s*/i, '').trim();
        
        if (inventory.includes(cardName.toLowerCase())) {
            inStock.push(cardName);
        } else {
            missing.push(cardName);
        }
    });
    
    document.getElementById('inStockList').innerHTML = inStock.map(card => `<li>${card}</li>`).join('');
    document.getElementById('missingList').innerHTML = missing.map(card => `<li>${card}</li>`).join('');

    btn.innerText = "Check Vault Inventory";
    btn.style.opacity = "1";
    btn.disabled = false;
}
</script>