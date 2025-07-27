# agents/inventory_checker.py

def check_inventory(state):
    parsed = state["parsed_order"]
    product = parsed["product"]
    quantity = parsed["quantity"]

    # Dummy inventory check
    stock_db = {"phones": 50, "laptops": 20, "chargers": 100, "tablets": 30, "headphones": 75, "speakers": 40, "cables": 200, "accessories": 150, "smartwatches": 60, "cameras": 25, "drones": 10, "gaming consoles": 15, "VR headsets": 5, "smart home devices": 80, "kitchen appliances": 90, "fitness trackers": 70, "audio equipment": 55, "computer components": 45, "networking devices": 65, "office supplies": 110, "furniture": 95, "toys": 85, "books": 120, "clothing": 130, "footwear": 140, "accessories": 150, "sports equipment": 75, "outdoor gear": 65, "pet supplies": 55, "healthcare products": 45, "beauty products": 35, "automotive parts": 25, "tools": 15, "gardening supplies": 5, "musical instruments": 80, "art supplies": 90, "craft materials": 100, "photography gear": 110, "video equipment": 120, "gaming accessories": 130, "collectibles": 140, "hobbies": 150, "seasonal items": 160, "gifts": 170, "electronics": 180, "appliances": 190, "furniture": 200}
    available = stock_db.get(product, 0)

    return {
        "inventory_ok": available >= quantity,
        "available_stock": available
    }
