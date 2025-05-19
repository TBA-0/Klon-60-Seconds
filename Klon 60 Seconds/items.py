import pygame
import json
import os
import random
from settings import *

class Item:
    def __init__(self, item_id, name, item_type, value, x=0, y=0, color=None):
        self.id = item_id
        self.name = name
        self.type = item_type
        self.value = value 
        self.x = x
        self.y = y
        self.width = ITEM_SIZE
        self.height = ITEM_SIZE
        self.rect = pygame.Rect(x, y, self.width, self.height)

        if color:
            self.color = color
        else:
            if item_type == "food":
                self.color = GREEN
            elif item_type == "water":
                self.color = BLUE
            elif item_type == "medical":
                self.color = WHITE
            elif item_type == "weapon":
                self.color = RED
            elif item_type == "tool":
                self.color = ORANGE
            elif item_type == "misc":
                self.color = YELLOW
            else:
                self.color = GRAY
    
    def update(self):
        """Update item state if needed"""
        pass
    
    def render(self, screen):
        """Render the item on the screen"""
        pygame.draw.rect(screen, self.color, self.rect)
        
    def set_position(self, x, y):
        """Set item position"""
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Inventory:
    def __init__(self):
        self.items = []
        self.max_items = MAX_INVENTORY
    
    def add_item(self, item):
        """Add item to inventory if there's space"""
        if len(self.items) < self.max_items:
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, item):
        """Remove item from inventory"""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def get_items(self):
        """Get all items in inventory"""
        return self.items
    
    def get_items_by_type(self, item_type):
        """Get items of a specific type"""
        return [item for item in self.items if item.type == item_type]
    
    def count_items_by_type(self, item_type):
        """Count items of a specific type"""
        return len(self.get_items_by_type(item_type))
    
    def has_item_type(self, item_type):
        """Check if inventory has at least one item of the given type"""
        return any(item.type == item_type for item in self.items)
    
    def clear(self):
        """Clear the inventory"""
        self.items = []


class ItemFactory:
    def __init__(self):
        self.items_data = []
        self.load_items_data()
    
    def load_items_data(self):
        """Load items data from JSON file"""
        try:
            if os.path.exists(ITEMS_FILE):
                with open(ITEMS_FILE, 'r') as f:
                    self.items_data = json.load(f)
            else:
                self.items_data = [
                    {"id": 1, "name": "Water Bottle", "type": "water", "value": 2},
                    {"id": 2, "name": "Canned Food", "type": "food", "value": 2},
                    {"id": 3, "name": "First Aid Kit", "type": "medical", "value": 3},
                    {"id": 4, "name": "Axe", "type": "weapon", "value": 2},
                    {"id": 5, "name": "Radio", "type": "tool", "value": 1},
                    {"id": 6, "name": "Map", "type": "misc", "value": 1},
                    {"id": 7, "name": "Flashlight", "type": "tool", "value": 1},
                    {"id": 8, "name": "Matches", "type": "tool", "value": 1},
                    {"id": 9, "name": "Gas Mask", "type": "misc", "value": 2},
                    {"id": 10, "name": "Rope", "type": "tool", "value": 1},
                    {"id": 11, "name": "Blanket", "type": "misc", "value": 1},
                    {"id": 12, "name": "Ammo", "type": "weapon", "value": 1},
                    {"id": 13, "name": "Pills", "type": "medical", "value": 2},
                    {"id": 14, "name": "Soup", "type": "food", "value": 1},
                    {"id": 15, "name": "Soda", "type": "water", "value": 1},
                ]

                os.makedirs(os.path.dirname(ITEMS_FILE), exist_ok=True)
                with open(ITEMS_FILE, 'w') as f:
                    json.dump(self.items_data, f, indent=4)
                    
        except Exception as e:
            print(f"Error loading items data: {e}")
            self.items_data = [
                {"id": 1, "name": "Water Bottle", "type": "water", "value": 2},
                {"id": 2, "name": "Canned Food", "type": "food", "value": 2},
                {"id": 3, "name": "First Aid Kit", "type": "medical", "value": 3}
            ]
    
    def create_random_item(self, x=0, y=0):
        """Create a random item from the available item types"""
        if not self.items_data:
            return None
            
        item_data = random.choice(self.items_data)
        return Item(
            item_data["id"],
            item_data["name"],
            item_data["type"],
            item_data["value"],
            x, y
        )
    
    def create_item_by_id(self, item_id, x=0, y=0):
        """Create a specific item by its ID"""
        for item_data in self.items_data:
            if item_data["id"] == item_id:
                return Item(
                    item_data["id"],
                    item_data["name"],
                    item_data["type"],
                    item_data["value"],
                    x, y
                )
        return None
