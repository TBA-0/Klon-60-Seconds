# Sprite and image generation for pygame

import pygame
import os
from settings import *

# Ensure the images directory exists
os.makedirs(IMAGES_DIR, exist_ok=True)

# Dictionary to store loaded sprites
sprites = {}

def create_simple_sprite(name, color, size, shape="rect"):
    """Create a simple colored sprite surface"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    if shape == "rect":
        pygame.draw.rect(surface, color, (0, 0, size, size))
    elif shape == "circle":
        pygame.draw.circle(surface, color, (size//2, size//2), size//2)
    return surface

def create_character_sprite(character_type):
    """Create a simple character sprite"""
    size = PLAYER_SIZE
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Base character shape (body)
    if character_type == "dad":
        body_color = (0, 0, 200)  # Blue
    elif character_type == "mom":
        body_color = (200, 0, 200)  # Purple
    elif character_type == "son":
        body_color = (0, 200, 0)  # Green
    elif character_type == "daughter":
        body_color = (200, 100, 0)  # Orange
    else:
        body_color = (150, 150, 150)  # Gray
    
    # Draw body
    pygame.draw.rect(surface, body_color, (5, 10, size - 10, size - 10))
    
    # Draw head
    head_size = size // 3
    pygame.draw.circle(surface, (255, 200, 150), (size//2, head_size), head_size)
    
    return surface

def create_item_sprite(item_type):
    """Create a simple item sprite based on type"""
    size = ITEM_SIZE
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    if item_type == "food":
        # Draw a simple food can
        pygame.draw.rect(surface, (150, 150, 150), (5, 3, size - 10, size - 6))
        pygame.draw.rect(surface, (0, 100, 0), (8, 6, size - 16, size - 12))
    elif item_type == "water":
        # Draw a water bottle
        pygame.draw.rect(surface, (100, 100, 255), (10, 5, size - 20, size - 10))
        pygame.draw.rect(surface, (150, 150, 255), (15, 3, size - 30, 5))
    elif item_type == "medical":
        # Draw a medical kit
        pygame.draw.rect(surface, (255, 255, 255), (5, 5, size - 10, size - 10))
        pygame.draw.rect(surface, (255, 0, 0), (size//2 - 2, 8, 4, size - 16))
        pygame.draw.rect(surface, (255, 0, 0), (8, size//2 - 2, size - 16, 4))
    elif item_type == "weapon":
        # Draw a simple weapon
        pygame.draw.rect(surface, (100, 50, 0), (5, size//2 - 3, size - 10, 6))
        pygame.draw.rect(surface, (100, 100, 100), (size - 15, size//2 - 5, 10, 10))
    elif item_type == "tool":
        # Draw a tool
        pygame.draw.rect(surface, (150, 150, 150), (5, 5, 10, size - 10))
        pygame.draw.rect(surface, (100, 50, 0), (15, size//2 - 5, size - 20, 10))
    else:  # misc or unknown
        # Draw a generic box
        pygame.draw.rect(surface, (200, 200, 0), (5, 5, size - 10, size - 10))
    
    return surface

def create_house_tiles():
    """Create simple tiles for the house"""
    tile_size = 50
    tiles = {}
    
    # Floor tile
    floor = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    floor_color = (200, 200, 200)
    pygame.draw.rect(floor, floor_color, (0, 0, tile_size, tile_size))
    # Add some texture
    for i in range(0, tile_size, 10):
        pygame.draw.line(floor, (180, 180, 180), (0, i), (tile_size, i), 1)
        pygame.draw.line(floor, (180, 180, 180), (i, 0), (i, tile_size), 1)
    tiles["floor"] = floor
    
    # Wall tile
    wall = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    wall_color = (100, 100, 100)
    pygame.draw.rect(wall, wall_color, (0, 0, tile_size, tile_size))
    # Add some texture
    for i in range(0, tile_size, 5):
        pygame.draw.line(wall, (80, 80, 80), (0, i), (tile_size, i), 1)
    tiles["wall"] = wall
    
    # Door tile
    door = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    door_color = (150, 75, 0)
    pygame.draw.rect(door, door_color, (0, 0, tile_size, tile_size))
    # Door handle
    pygame.draw.circle(door, (200, 200, 0), (tile_size - 10, tile_size//2), 3)
    tiles["door"] = door
    
    return tiles

def load_sprites():
    """Load or create all needed sprites"""
    global sprites
    
    # Create character sprites
    sprites["player"] = create_character_sprite("dad")
    sprites["mom"] = create_character_sprite("mom")
    sprites["son"] = create_character_sprite("son")
    sprites["daughter"] = create_character_sprite("daughter")
    
    # Create item sprites
    sprites["food"] = create_item_sprite("food")
    sprites["water"] = create_item_sprite("water")
    sprites["medical"] = create_item_sprite("medical")
    sprites["weapon"] = create_item_sprite("weapon")
    sprites["tool"] = create_item_sprite("tool")
    sprites["misc"] = create_item_sprite("misc")
    
    # Create house tiles
    house_tiles = create_house_tiles()
    sprites.update(house_tiles)
    
    return sprites

# Function to get a sprite by name
def get_sprite(name):
    """Get a sprite by name, loading all sprites if necessary"""
    global sprites
    if not sprites:
        sprites = load_sprites()
    
    return sprites.get(name, None)
