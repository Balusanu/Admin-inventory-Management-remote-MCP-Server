from fastmcp import FastMCP
from database import SessionLocal, engine
from models import Base, Item

Base.metadata.create_all(bind=engine)

mcp = FastMCP("Office Admin Inventory")

# -------------------
# Add Item
# -------------------
@mcp.tool()
def add_item(name: str, category: str, quantity: int, min_threshold: int):
    db = SessionLocal()
    existing = db.query(Item).filter(Item.name == name).first()

    if existing:
        return "Item already exists."

    item = Item(
        name=name,
        category=category,
        quantity=quantity,
        min_threshold=min_threshold
    )

    db.add(item)
    db.commit()
    return f"{name} added successfully."

# -------------------
# Issue Item
# -------------------
@mcp.tool()
def issue_item(name: str, quantity: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.name == name).first()

    if not item:
        return "Item not found."

    if item.quantity < quantity:
        return "Insufficient stock."

    item.quantity -= quantity
    db.commit()

    if item.quantity <= item.min_threshold:
        return f"Issued. ⚠ Low stock! Only {item.quantity} left."

    return f"Issued successfully. Remaining: {item.quantity}"

# -------------------
# Check Stock
# -------------------
@mcp.tool()
def check_stock(name: str):
    db = SessionLocal()
    item = db.query(Item).filter(Item.name == name).first()

    if not item:
        return "Item not found."

    return {
        "name": item.name,
        "category": item.category,
        "quantity": item.quantity,
        "min_threshold": item.min_threshold
    }

# -------------------
# List Items
# -------------------
@mcp.tool()
def list_items():
    db = SessionLocal()
    items = db.query(Item).all()

    return [
        {
            "name": i.name,
            "category": i.category,
            "quantity": i.quantity
        }
        for i in items
    ]

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)