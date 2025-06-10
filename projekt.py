import pygame
import sys
import os
import random
import time
import json

os.makedirs("assets/data", exist_ok=True)
os.makedirs("assets/fonts", exist_ok=True)
os.makedirs("assets/images", exist_ok=True)
WIDTH = 1280
HEIGHT = 720
FPS = 60
TITLE = "60 Sekund Klon"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
BROWN = (165, 42, 42)
DARK_BROWN = (101, 67, 33)
ORANGE = (255, 165, 0)

MENU = "menu"
SCAVENGING = "scavenging"
SURVIVAL = "survival"
GAME_OVER = "game_over"
PAUSE = "pause"
USE_POLISH = True
SCAVENGING_TIME = 60 
PLAYER_SPEED = 5
PLAYER_SIZE = 40
HOUSE_WIDTH = 800
HOUSE_HEIGHT = 600
ROOM_SIZE = 150
WALL_THICKNESS = 10
ITEM_SIZE = 30
MAX_INVENTORY = 20
FONT_SIZE_SMALL = 20
FONT_SIZE_MEDIUM = 30
FONT_SIZE_LARGE = 50
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
UI_PADDING = 20
DAYS_TO_WIN = 30 
START_FOOD = 3
START_WATER = 3
MAX_HEALTH = 100
MAX_SANITY = 100
FOOD_CONSUMPTION_RATE = 1  
WATER_CONSUMPTION_RATE = 1  
HEALTH_DECREASE_RATE = 10  
SANITY_DECREASE_RATE = 5  

ASSET_DIR = "assets"
IMAGES_DIR = f"{ASSET_DIR}/images"
FONTS_DIR = f"{ASSET_DIR}/fonts"
DATA_DIR = f"{ASSET_DIR}/data"

ITEMS_FILE = f"{DATA_DIR}/items.json"
EVENTS_FILE = f"{DATA_DIR}/events.json"
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
    
    if character_type == "dad":
        body_color = (0, 0, 200)  
    elif character_type == "mom":
        body_color = (200, 0, 200)  
    elif character_type == "son":
        body_color = (0, 200, 0)  
    elif character_type == "daughter":
        body_color = (200, 100, 0) 
    else:
        body_color = (150, 150, 150) 
    
    pygame.draw.rect(surface, body_color, (5, 10, size - 10, size - 10))
    
    head_size = size // 3
    pygame.draw.circle(surface, (255, 200, 150), (size//2, head_size), head_size)
    
    return surface

def create_item_sprite(item_type):
    """Create a simple item sprite based on type"""
    size = ITEM_SIZE
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    if item_type == "food":
        pygame.draw.rect(surface, (150, 150, 150), (5, 3, size - 10, size - 6))
        pygame.draw.rect(surface, (0, 100, 0), (8, 6, size - 16, size - 12))
    elif item_type == "water":
        pygame.draw.rect(surface, (100, 100, 255), (10, 5, size - 20, size - 10))
        pygame.draw.rect(surface, (150, 150, 255), (15, 3, size - 30, 5))
    elif item_type == "medical":
        pygame.draw.rect(surface, (255, 255, 255), (5, 5, size - 10, size - 10))
        pygame.draw.rect(surface, (255, 0, 0), (size//2 - 2, 8, 4, size - 16))
        pygame.draw.rect(surface, (255, 0, 0), (8, size//2 - 2, size - 16, 4))
    elif item_type == "weapon":
        pygame.draw.rect(surface, (100, 50, 0), (5, size//2 - 3, size - 10, 6))
        pygame.draw.rect(surface, (100, 100, 100), (size - 15, size//2 - 5, 10, 10))
    elif item_type == "tool":
        pygame.draw.rect(surface, (150, 150, 150), (5, 5, 10, size - 10))
        pygame.draw.rect(surface, (100, 50, 0), (15, size//2 - 5, size - 20, 10))
    else:  
        pygame.draw.rect(surface, (200, 200, 0), (5, 5, size - 10, size - 10))
    
    return surface

def create_house_tiles():
    """Create simple tiles for the house"""
    tile_size = 50
    tiles = {}
    
    floor = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    floor_color = (200, 200, 200)
    pygame.draw.rect(floor, floor_color, (0, 0, tile_size, tile_size))
    for i in range(0, tile_size, 10):
        pygame.draw.line(floor, (180, 180, 180), (0, i), (tile_size, i), 1)
        pygame.draw.line(floor, (180, 180, 180), (i, 0), (i, tile_size), 1)
    tiles["floor"] = floor
    
    wall = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    wall_color = (100, 100, 100)
    pygame.draw.rect(wall, wall_color, (0, 0, tile_size, tile_size))
    for i in range(0, tile_size, 5):
        pygame.draw.line(wall, (80, 80, 80), (0, i), (tile_size, i), 1)
    tiles["wall"] = wall
    
    door = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    door_color = (150, 75, 0)
    pygame.draw.rect(door, door_color, (0, 0, tile_size, tile_size))
    pygame.draw.circle(door, (200, 200, 0), (tile_size - 10, tile_size//2), 3)
    tiles["door"] = door
    
    return tiles

def load_sprites():
    """Load or create all needed sprites"""
    global sprites
    sprites["player"] = create_character_sprite("dad")
    sprites["mom"] = create_character_sprite("mom")
    sprites["son"] = create_character_sprite("son")
    sprites["daughter"] = create_character_sprite("daughter")
    sprites["food"] = create_item_sprite("food")
    sprites["water"] = create_item_sprite("water")
    sprites["medical"] = create_item_sprite("medical")
    sprites["weapon"] = create_item_sprite("weapon")
    sprites["tool"] = create_item_sprite("tool")
    sprites["misc"] = create_item_sprite("misc")
    
    house_tiles = create_house_tiles()
    sprites.update(house_tiles)
    
    return sprites

def get_sprite(name):
    """Get a sprite by name, loading all sprites if necessary"""
    global sprites
    if not sprites:
        sprites = load_sprites()
    
    return sprites.get(name, None)
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = BLUE
        
        self.direction = "down" 
        
        self.current_frame = 0
        self.animation_timer = 0
        self.moving = False
        
        self.carrying_item = None
        
        self.health = MAX_HEALTH
        self.sanity = MAX_SANITY
        self.is_injured = False
        self.is_sick = False
        self.is_tired = False
        
    def move(self, keys):
        """Handle player movement based on keyboard input"""
        self.moving = False
        
        dx = 0
        dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"
            self.moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"
            self.moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
            self.direction = "up"
            self.moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            self.direction = "down"
            self.moving = True
            
        new_rect = self.rect.copy()
        new_rect.x += dx
        new_rect.y += dy
        
        if new_rect.left < 0:
            new_rect.left = 0
        if new_rect.right > WIDTH:
            new_rect.right = WIDTH
        if new_rect.top < 0:
            new_rect.top = 0
        if new_rect.bottom > HEIGHT:
            new_rect.bottom = HEIGHT
            
        self.rect = new_rect
        self.x = self.rect.x
        self.y = self.rect.y
        
        if self.moving:
            self.animation_timer += 1
            if self.animation_timer >= 5: 
                self.current_frame = (self.current_frame + 1) % 4  
                self.animation_timer = 0
    
    def pick_up_item(self, item):
        """Pick up an item if not already carrying one"""
        if self.carrying_item is None:
            self.carrying_item = item
            return True
        return False
    
    def drop_item(self):
        """Drop the currently carried item"""
        item = self.carrying_item
        self.carrying_item = None
        return item
        
    def update(self):
        """Update player state"""
        keys = pygame.key.get_pressed()
        
        self.move(keys)
        
    def render(self, screen):
        """Render the player on the screen"""
        pygame.draw.rect(screen, self.color, self.rect)
        
        if self.carrying_item:
            item_rect = pygame.Rect(
                self.rect.x + (self.rect.width - ITEM_SIZE) // 2,
                self.rect.y - ITEM_SIZE - 5,
                ITEM_SIZE, 
                ITEM_SIZE
            )
            pygame.draw.rect(screen, self.carrying_item.color, item_rect)
    
    def set_position(self, x, y):
        """Set player position"""
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
    def collides_with(self, rect):
        """Check if player collides with a rectangle"""
        return self.rect.colliderect(rect)

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
        """Load items data from JSON file or create default items"""
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

class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_GRAY, hover_color=GRAY, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.action = None
    
    def set_action(self, action):
        """Set the action to be returned when clicked"""
        self.action = action
        return self
    
    def update(self, mouse_pos):
        """Update button state based on mouse position"""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def render(self, screen):
        """Render the button"""
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2) 
        
        font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_click(self, mouse_pos):
        """Check if button is clicked and return its action"""
        if self.rect.collidepoint(mouse_pos):
            return self.action
        return None


class UI:
    def __init__(self):
        self.buttons = []
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
    
    def handle_event(self, event):
        """Handle UI events and return actions"""
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.update(event.pos)
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            for button in self.buttons:
                action = button.check_click(event.pos)
                if action:
                    return action
        
        return None
    
    def render_menu(self, screen):
        """Render the main menu"""
        self.buttons = []
        
        screen.fill(DARK_GRAY)
        
        title = "60 SEKUND KLON"
        title_text = self.font_large.render(title, True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(title_text, title_rect)
        
        subtitle = "Remake w Pygame/Python"
        subtitle_text = self.font_medium.render(subtitle, True, LIGHT_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 60))
        screen.blit(subtitle_text, subtitle_rect)
        
        start_text = "Rozpocznij Grę"
        start_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT//2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            start_text
        ).set_action("start_game")
        
        quit_text = "Wyjdź"
        quit_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT//2 + BUTTON_HEIGHT + 20,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            quit_text
        ).set_action("quit")
        
        self.buttons.extend([start_button, quit_button])
        
        for button in self.buttons:
            button.render(screen)
            
        instructions = [
            "W 60 SEKUND musisz:",
            "1. Zdobyć zapasy z domu w 60 sekund",
            "2. Przetrwać w schronie jak najdłużej",
            "Użyj WASD lub strzałek do poruszania się",
            "Naciśnij SPACJĘ aby podnieść/upuścić przedmioty"
        ]
        
        y_offset = HEIGHT * 3/4
        for instruction in instructions:
            text = self.font_small.render(instruction, True, WHITE)
            rect = text.get_rect(center=(WIDTH//2, y_offset))
            screen.blit(text, rect)
            y_offset += 30
    
    def render_pause_menu(self, screen):
        """Render the pause menu overlay"""
        self.buttons = []
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  
        screen.blit(overlay, (0, 0))
        
        pause_text = self.font_large.render("PAUZA", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(pause_text, pause_rect)
        
        resume_text = "Kontynuuj"
        resume_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT//2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            resume_text
        ).set_action("resume")
        
        menu_text = "Menu Główne"
        menu_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT//2 + BUTTON_HEIGHT + 20,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            menu_text
        ).set_action("main_menu")
        
        quit_text = "Wyjdź"
        quit_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT//2 + (BUTTON_HEIGHT + 20) * 2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            quit_text
        ).set_action("quit")
        
        self.buttons.extend([resume_button, menu_button, quit_button])
        
        for button in self.buttons:
            button.render(screen)
    
    def render_scavenging_ui(self, screen, time_left, inventory):
        """Render UI elements for the scavenging phase"""
        time_text = self.font_large.render(f"{time_left}", True, WHITE if time_left > 10 else RED)
        time_rect = time_text.get_rect(topright=(WIDTH - UI_PADDING, UI_PADDING))
        screen.blit(time_text, time_rect)
        timer_label_text = "POZOSTAŁO SEKUND"
        timer_label = self.font_small.render(timer_label_text, True, WHITE)
        timer_label_rect = timer_label.get_rect(topright=(WIDTH - UI_PADDING, UI_PADDING + time_rect.height))
        screen.blit(timer_label, timer_label_rect)
        
        inventory_label = "Przedmioty:"
        inventory_text = self.font_medium.render(f"{inventory_label} {len(inventory.items)}/{inventory.max_items}", True, WHITE)
        inventory_rect = inventory_text.get_rect(topleft=(UI_PADDING, UI_PADDING))
        screen.blit(inventory_text, inventory_rect)
        
        controls_text = self.font_small.render("WASD/Strzałki: Ruch   SPACJA: Podnieś/Upuść", True, WHITE)
        controls_rect = controls_text.get_rect(midbottom=(WIDTH//2, HEIGHT - UI_PADDING))
        screen.blit(controls_text, controls_rect)

    def render_game_over(self, screen, days_survived, reason):
        """Render game over screen"""
        self.buttons = []
        screen.fill(DARK_GRAY)
        

        game_over_text = self.font_large.render("KONIEC GRY", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(game_over_text, game_over_rect)
        
        days_label = "Dni Przetrwane:"
        days_text = self.font_medium.render(f"{days_label} {days_survived}", True, WHITE)
        days_rect = days_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 80))
        screen.blit(days_text, days_rect)
        
        if "survived all 30 days" in reason:
            reason = "Przetrwałeś wszystkie 30 dni! Wygrałeś!"
        elif "has died" in reason:
            name = reason.split(" ")[0]
            reason = f"{name} nie żyje. Koniec gry."
        elif "entire family has died" in reason:
            reason = "Cała rodzina zmarła. Koniec gry."
        words = reason.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if self.font_medium.size(test_line)[0] > WIDTH - 100:
                current_line.pop() 
                lines.append(' '.join(current_line))
                current_line = [word]  
        
        if current_line: 
            lines.append(' '.join(current_line))
        
        y_offset = HEIGHT//4 + 140
        for line in lines:
            reason_text = self.font_medium.render(line, True, LIGHT_GRAY)
            reason_rect = reason_text.get_rect(center=(WIDTH//2, y_offset))
            screen.blit(reason_text, reason_rect)
            y_offset += 40
        restart_text = "Nowa Gra"
        restart_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT * 3//4,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            restart_text
        ).set_action("start_game")
        
        menu_text = "Menu Główne"
        menu_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT * 3//4 + BUTTON_HEIGHT + 20,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            menu_text
        ).set_action("main_menu")
        
        self.buttons.extend([restart_button, menu_button])
        for button in self.buttons:
            button.render(screen)

class Room:
    def __init__(self, x, y, width, height, room_type="generic"):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = room_type
        self.color = LIGHT_GRAY
        self.items = []
        self.walls = []
        self.doors = []
        
        self._create_walls()
    
    def _create_walls(self):
        """Create walls for the room"""
        self.walls.append(pygame.Rect(
            self.rect.x, self.rect.y,
            self.rect.width, WALL_THICKNESS
        ))
        
        self.walls.append(pygame.Rect(
            self.rect.x, self.rect.y + self.rect.height - WALL_THICKNESS,
            self.rect.width, WALL_THICKNESS
        ))
        
        self.walls.append(pygame.Rect(
            self.rect.x, self.rect.y,
            WALL_THICKNESS, self.rect.height
        ))
        self.walls.append(pygame.Rect(
            self.rect.x + self.rect.width - WALL_THICKNESS, self.rect.y,
            WALL_THICKNESS, self.rect.height
        ))
    
    def add_door(self, direction):
        """Add a door to the room in the specified direction"""
        door_width = ROOM_SIZE // 4
        
        if direction == "top":
            door = pygame.Rect(
                self.rect.centerx - door_width // 2,
                self.rect.y,
                door_width, WALL_THICKNESS
            )
        elif direction == "bottom":
            door = pygame.Rect(
                self.rect.centerx - door_width // 2,
                self.rect.y + self.rect.height - WALL_THICKNESS,
                door_width, WALL_THICKNESS
            )
        elif direction == "left":
            door = pygame.Rect(
                self.rect.x,
                self.rect.centery - door_width // 2,
                WALL_THICKNESS, door_width
            )
        else:  
            door = pygame.Rect(
                self.rect.x + self.rect.width - WALL_THICKNESS,
                self.rect.centery - door_width // 2,
                WALL_THICKNESS, door_width
            )
            
        self.doors.append({
            "rect": door,
            "direction": direction
        })
    
    def add_item(self, item):
        """Add an item to the room"""
        self.items.append(item)
    
    def remove_item(self, item):
        """Remove an item from the room"""
        if item in self.items:
            self.items.remove(item)
    
    def render(self, screen):
        """Render the room and its contents"""
        pygame.draw.rect(screen, self.color, self.rect)
        
        for wall in self.walls:
            pygame.draw.rect(screen, DARK_GRAY, wall)
        
        for door in self.doors:
            pygame.draw.rect(screen, BROWN, door["rect"])
        
        for item in self.items:
            item.render(screen)
            
    def get_collision_walls(self):
        """Get walls for collision detection"""
        collision_walls = []
        
        for wall in self.walls:
            include = True
            for door in self.doors:
                if wall.colliderect(door["rect"]):
                    include = False
                    if door["direction"] == "top" or door["direction"] == "bottom":
                        left_segment = pygame.Rect(
                            wall.x, wall.y,
                            door["rect"].x - wall.x, wall.height
                        )
                        right_segment = pygame.Rect(
                            door["rect"].x + door["rect"].width, wall.y,
                            wall.x + wall.width - (door["rect"].x + door["rect"].width), wall.height
                        )
                        collision_walls.extend([left_segment, right_segment])
                    else:  
                        top_segment = pygame.Rect(
                            wall.x, wall.y,
                            wall.width, door["rect"].y - wall.y
                        )
                        bottom_segment = pygame.Rect(
                            wall.x, door["rect"].y + door["rect"].height,
                            wall.width, wall.y + wall.height - (door["rect"].y + door["rect"].height)
                        )
                        collision_walls.extend([top_segment, bottom_segment])
                    break
            
            if include:
                collision_walls.append(wall)
                
        return collision_walls

class House:
    def __init__(self):
        self.rooms = []
        self.generate_layout()
        self.item_factory = ItemFactory()
        self.populate_rooms()
        
    def generate_layout(self):
        """Generate the house layout with multiple rooms"""
        
        start_x = (WIDTH - HOUSE_WIDTH) // 2
        start_y = (HEIGHT - HOUSE_HEIGHT) // 2
        
        room_width = HOUSE_WIDTH // 3
        room_height = HOUSE_HEIGHT // 2
        
        room_types = [
            "kitchen", "living_room", "bedroom",
            "bathroom", "storage", "garage"
        ]
        
        for row in range(2):
            for col in range(3):
                room_index = row * 3 + col
                room_type = room_types[room_index]
                
                room = Room(
                    start_x + col * room_width,
                    start_y + row * room_height,
                    room_width,
                    room_height,
                    room_type
                )
            
                if col > 0:  
                    room.add_door("left")
                    self.rooms[room_index - 1].add_door("right")
                    
                if row > 0: 
                    room.add_door("top")
                    self.rooms[room_index - 3].add_door("bottom")
                
                self.rooms.append(room)
    
    def populate_rooms(self):
        """Add random items to rooms"""
        items_per_room = {
            "kitchen": (3, 5),
            "living_room": (2, 4),
            "bedroom": (1, 3),
            "bathroom": (1, 3),
            "storage": (4, 6),
            "garage": (2, 4)
        }
        
        for room in self.rooms:
            min_items, max_items = items_per_room.get(room.type, (1, 3))
            num_items = random.randint(min_items, max_items)
            
            for _ in range(num_items):
                valid_position = False
                item = None
                
                while not valid_position:
                    padding = ITEM_SIZE
                    x = random.randint(
                        room.rect.x + padding,
                        room.rect.x + room.rect.width - padding - ITEM_SIZE
                    )
                    y = random.randint(
                        room.rect.y + padding,
                        room.rect.y + room.rect.height - padding - ITEM_SIZE
                    )
                    
                    item = self.item_factory.create_random_item(x, y)
                    
                    overlap = False
                    for existing_item in room.items:
                        if item.rect.colliderect(existing_item.rect):
                            overlap = True
                            break
                    
                    if not overlap:
                        valid_position = True
                
                room.add_item(item)
    
    def render(self, screen):
        """Render the house and all rooms"""
        for room in self.rooms:
            room.render(screen)
    
    def get_all_items(self):
        """Get all items in the house"""
        all_items = []
        for room in self.rooms:
            all_items.extend(room.items)
        return all_items
    
    def get_all_wall_colliders(self):
        """Get all wall colliders in the house"""
        all_walls = []
        for room in self.rooms:
            all_walls.extend(room.get_collision_walls())
        return all_walls
    
    def remove_item(self, item):
        """Remove an item from its room"""
        for room in self.rooms:
            if item in room.items:
                room.remove_item(item)
                return True
        return False
    

class ScavengingPhase:
    def __init__(self, player, inventory):
        self.player = player
        self.inventory = inventory
        self.house = House()
        
        self.player.set_position(WIDTH // 2, HEIGHT // 2)
        self.interaction_radius = PLAYER_SIZE + ITEM_SIZE
    
    def handle_event(self, event):
        """Handle events for the scavenging phase"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.handle_interaction()
    
    def handle_interaction(self):
        """Handle player interaction with items"""
        if self.player.carrying_item:
            item = self.player.drop_item()
            added = self.inventory.add_item(item)
            if not added:
                item.set_position(
                    self.player.rect.x + random.randint(-50, 50),
                    self.player.rect.y + random.randint(-50, 50)
                )
                self.house.rooms[0].add_item(item) 
        else:
            for item in self.house.get_all_items():
                distance = ((self.player.rect.centerx - item.rect.centerx) ** 2 + 
                           (self.player.rect.centery - item.rect.centery) ** 2) ** 0.5
                
                if distance <= self.interaction_radius:
                    picked_up = self.player.pick_up_item(item)
                    if picked_up:
                        self.house.remove_item(item)
                        break
    
    def check_collisions(self):
        """Check and resolve collisions with walls"""
        player_rect = self.player.rect
        for wall in self.house.get_all_wall_colliders():
            if player_rect.colliderect(wall):
                overlap_x = min(
                    player_rect.right - wall.left,
                    wall.right - player_rect.left
                )
                overlap_y = min(
                    player_rect.bottom - wall.top,
                    wall.bottom - player_rect.top
                )
                
                if overlap_x < overlap_y:
                    if player_rect.centerx < wall.centerx:
                        player_rect.right = wall.left
                    else:
                        player_rect.left = wall.right
                else:
                    if player_rect.centery < wall.centery:
                        player_rect.bottom = wall.top
                    else:
                        player_rect.top = wall.bottom
                        
    
    def update(self):
        """Update the scavenging phase state"""
        self.player.update()
        
        self.check_collisions()
    
    def render(self, screen):
        """Render the scavenging phase"""
        screen.fill(BLACK)
        
        self.house.render(screen)
        
        self.player.render(screen)

class SurvivalCharacter:
    def __init__(self, name, image_key):
        self.name = name
        self.image_key = image_key
        self.health = MAX_HEALTH
        self.sanity = MAX_SANITY
        self.hunger = 100  
        self.thirst = 100  
        self.is_alive = True
        self.is_sick = False
        self.is_injured = False
        self.is_insane = False
        self.days_hungry = 0
        self.days_thirsty = 0
    
    def update_stats(self, food_consumed=0, water_consumed=0):
        """Update character stats for a new day"""

        self.hunger = min(100, self.hunger + food_consumed * 25)
        if self.hunger <= 0:
            self.days_hungry += 1
            self.health -= HEALTH_DECREASE_RATE
            self.sanity -= SANITY_DECREASE_RATE // 2
        else:
            self.days_hungry = 0
            
        self.thirst = min(100, self.thirst + water_consumed * 25)
        if self.thirst <= 0:
            self.days_thirsty += 1
            self.health -= HEALTH_DECREASE_RATE * 1.5 
            self.sanity -= SANITY_DECREASE_RATE // 2
        else:
            self.days_thirsty = 0
            
        self.hunger -= 25
        self.thirst -= 33 
        
        self.health = max(0, min(MAX_HEALTH, self.health))
        self.sanity = max(0, min(MAX_SANITY, self.sanity))
        
        if self.health <= 0:
            self.is_alive = False
            
        self.is_insane = self.sanity <= 15
        
        if self.hunger > 50 and self.thirst > 50 and not self.is_sick and not self.is_injured:
            self.health = min(MAX_HEALTH, self.health + 5)
            
        if self.hunger > 70 and self.thirst > 70 and self.health > 70:
            self.sanity = min(MAX_SANITY, self.sanity + 5)
    
    def consume_food(self, amount):
        """Consume food and update hunger"""
        self.hunger = min(100, self.hunger + amount * 25)
        
    def consume_water(self, amount):
        """Consume water and update thirst"""
        self.thirst = min(100, self.thirst + amount * 25)
        
    def apply_medical(self):
        """Apply medical treatment"""
        if self.is_sick or self.is_injured:
            self.is_sick = False
            self.is_injured = False
            self.health = min(MAX_HEALTH, self.health + 20)
            return True
        return False
    
    def status_summary(self):
        """Get a summary of the character's status"""
        status = []
        
        if self.health >= 80:
            status.append("Zdrowy")
        elif self.health >= 50:
            status.append("Lekkie obrażenia")
        elif self.health >= 25:
            status.append("Poważnie ranny")
        else:
            status.append("Stan krytyczny")
        
        if self.hunger <= 0:
            status.append("Głoduje")
        elif self.hunger <= 25:
            status.append("Bardzo głodny")
        elif self.hunger <= 50:
            status.append("Głodny")
            
        if self.thirst <= 0:
            status.append("Odwodniony")
        elif self.thirst <= 25:
            status.append("Bardzo spragniony")
        elif self.thirst <= 50:
            status.append("Spragniony")
            
        if self.is_sick:
            status.append("Chory")
        if self.is_injured:
            status.append("Ranny")
        if self.is_insane:
            status.append("Obłąkany")
            
        return status

class Event:
    def __init__(self, event_id, title, description, choices, condition=None, priority=0):
        self.id = event_id
        self.title = title
        self.description = description
        self.choices = choices  
        self.condition = condition  
        self.priority = priority 
        
    def get_outcome(self, choice_index):
        """Get the outcome for the selected choice"""
        if choice_index < 0 or choice_index >= len(self.choices):
            return None
        return self.choices[choice_index]["outcome"]
    
    def meets_condition(self, day, people_alive, food, water, weapons, tools):
        """Check if event meets conditions to occur"""
        if not self.condition:
            return True
            
        condition = self.condition
        
        if "min_day" in condition and day < condition["min_day"]:
            return False
            

        if "max_day" in condition and day > condition["max_day"]:
            return False
            

        if "min_people" in condition and people_alive < condition["min_people"]:
            return False
            
        if "min_food" in condition and food < condition["min_food"]:
            return False
        if "min_water" in condition and water < condition["min_water"]:
            return False
        if "min_weapons" in condition and weapons < condition["min_weapons"]:
            return False
        if "min_tools" in condition and tools < condition["min_tools"]:
            return False
            
        if "max_food" in condition and food > condition["max_food"]:
            return False
        if "max_water" in condition and water > condition["max_water"]:
            return False
            
        return True

class EventManager:
    def __init__(self):
        self.events = []
        self.load_events()
    
    def load_events(self):
        """Load events from JSON file or create default events"""
        self.create_default_events()
    
    def create_default_events(self):
        """Create and save default events"""
        self.events = [
            Event(
                1,
                "Burza Radiacyjna",
                "Nadciąga burza radiacyjna. Powinieneś przygotować swój schron.",
                [
                    {
                        "text": "Zamknij całą wentylację",
                        "outcome": {
                            "message": "Zamknąłeś całą wentylację. Powietrze staje się nieświeże, ale jesteś bezpieczny przed promieniowaniem.",
                            "effects": [
                                {"type": "sanity", "value": -5, "target": "all"}
                            ]
                        }
                    },
                    {
                        "text": "Zostaw wentylację otwartą",
                        "outcome": {
                            "message": "Zostawiłeś wentylację otwartą. Powietrze jest świeże, ale dostało się trochę promieniowania.",
                            "effects": [
                                {"type": "health", "value": -10, "target": "all"}
                            ]
                        }
                    }
                ],
                priority=2
            ),
            Event(
                2,
                "Dziwne Dźwięki",
                "Słyszysz dziwne dźwięki na zewnątrz schronu. To mogą być ocaleni, zwierzęta lub coś gorszego.",
                [
                    {
                        "text": "Zbadaj (Wyślij Tatę)",
                        "outcome": {
                            "message": "Tata zbadał hałas. To był tylko wiatr, ale znalazł trochę zapasów!",
                            "effects": [
                                {"type": "food", "value": 1},
                                {"type": "health", "value": -5, "target": "dad"}
                            ]
                        }
                    },
                    {
                        "text": "Zignoruj to",
                        "outcome": {
                            "message": "Postanowiłeś zignorować hałas. Lepiej dmuchać na zimne.",
                            "effects": [
                                {"type": "sanity", "value": -3, "target": "all"}
                            ]
                        }
                    }
                ]
            ),
            Event(
                3,
                "Niedobór Jedzenia",
                "Twoje zapasy jedzenia są niebezpiecznie niskie.",
                [
                    {
                        "text": "Racjonuj jedzenie",
                        "outcome": {
                            "message": "Postanowiłeś racjonować jedzenie. Wszyscy są głodni, ale przetrwają dłużej.",
                            "effects": [
                                {"type": "sanity", "value": -5, "target": "all"}
                            ]
                        }
                    },
                    {
                        "text": "Wyślij kogoś po zapasy (Mamę)",
                        "outcome": {
                            "message": "Mama poszła szukać zapasów i znalazła konserwy, ale została ranna.",
                            "effects": [
                                {"type": "food", "value": 2},
                                {"type": "health", "value": -15, "target": "mom"}
                            ]
                        }
                    }
                ],
                condition={"max_food": 2},
                priority=3
            ),
            Event(
                4,
                "Szczury w Schronie",
                "Szczury dostały się do schronu i zagrażają zapasowi jedzenia.",
                [
                    {
                        "text": "Postaw pułapki",
                        "outcome": {
                            "message": "Postawiłeś pułapki i złapałeś większość szczurów. Twoje jedzenie jest bezpieczne.",
                            "effects": []
                        }
                    },
                    {
                        "text": "Poluj na nie bronią",
                        "outcome": {
                            "message": "Upolowałeś szczury bronią. Pozbyłeś się ich i nawet udało ci się ugotować niektóre na dodatkowe jedzenie.",
                            "effects": [
                                {"type": "food", "value": 1},
                                {"type": "weapons", "value": -1}
                            ]
                        }
                    },
                    {
                        "text": "Zignoruj je",
                        "outcome": {
                            "message": "Zignorowałeś szczury. Zjadły część twoich zapasów jedzenia.",
                            "effects": [
                                {"type": "food", "value": -2}
                            ]
                        }
                    }
                ]
            ),
            Event(
                5,
                "Kłótnia Rodzinna",
                "Napięcie w schronie doprowadziło do ostrej kłótni między członkami rodziny.",
                [
                    {
                        "text": "Spróbuj mediować",
                        "outcome": {
                            "message": "Udało ci się uspokoić wszystkich. Rodzina czuje się teraz bardziej zjednoczona.",
                            "effects": [
                                {"type": "sanity", "value": 5, "target": "all"}
                            ]
                        }
                    },
                    {
                        "text": "Stań po czyjejś stronie",
                        "outcome": {
                            "message": "Stanąłeś po stronie w kłótni. To spowodowało większy podział w rodzinie.",
                            "effects": [
                                {"type": "sanity", "value": -10, "target": "all"}
                            ]
                        }
                    },
                    {
                        "text": "Zignoruj konflikt",
                        "outcome": {
                            "message": "Zignorowałeś konflikt. Kłótnia w końcu ucichła, ale pozostała uraza.",
                            "effects": [
                                {"type": "sanity", "value": -5, "target": "all"}
                            ]
                        }
                    }
                ],
                condition={"min_day": 7}
            )
        ]
    
    def get_random_events(self, day, people_alive, food, water, weapons, tools, max_events=2):
        """Get random events that can occur on the current day"""
        possible_events = []
        
        for event in self.events:
            if event.meets_condition(day, people_alive, food, water, weapons, tools):
                possible_events.append(event)
        if not possible_events:
            return []
            
        possible_events.sort(key=lambda e: e.priority, reverse=True)
        num_events = min(len(possible_events), max_events)
        return random.sample(possible_events, num_events)

class SurvivalPhase:
    def __init__(self, inventory):
        self.inventory = inventory
        self.event_manager = EventManager()
        
        self.family = [
            SurvivalCharacter("Dad", "dad"),
            SurvivalCharacter("Mom", "mom"),
            SurvivalCharacter("Son", "son"),
            SurvivalCharacter("Daughter", "daughter")
        ]
        
        self.food = 0
        self.water = 0
        self.medical = 0
        self.weapons = 0
        self.tools = 0
        self.misc = 0
        
        self.current_day = 1
        self.current_events = []
        self.resolved_events = []
        
        self.selected_character = None
        self.active_panel = "main"  
        self.event_choice = None
        
        self.buttons = []
    
    def initialize(self, inventory_items):
        """Initialize survival phase with collected inventory items"""
        for item in inventory_items:
            if item.type == "food":
                self.food += item.value
            elif item.type == "water":
                self.water += item.value
            elif item.type == "medical":
                self.medical += item.value
            elif item.type == "weapon":
                self.weapons += item.value
            elif item.type == "tool":
                self.tools += item.value
            elif item.type == "misc":
                self.misc += item.value
        
        self.food = max(self.food, 1) 
        self.water = max(self.water, 1)
    
        self.generate_new_events()
    
    def handle_event(self, event):
        """Handle events for the survival phase"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    action = button["action"]
                    data = button.get("data")
                    if action == "next_day":
                        return "next_day"
                    else:
                        self.process_button_action(action, data)
        return None
    
    def process_button_action(self, action, data=None):
        """Process button actions"""
        if action == "view_character":
            self.active_panel = "character"
            self.selected_character = data
        elif action == "view_event":
            self.active_panel = "event"
            self.event_choice = data
        elif action == "view_inventory":
            self.active_panel = "inventory"
        elif action == "back_to_main":
            self.active_panel = "main"
        elif action == "consume_food":
            if self.food > 0:
                self.food -= 1
                self.selected_character.consume_food(1)
        elif action == "consume_water":
            if self.water > 0:
                self.water -= 1
                self.selected_character.consume_water(1)
        elif action == "use_medical":
            if self.medical > 0:
                if self.selected_character.apply_medical():
                    self.medical -= 1
        elif action == "resolve_event":
            self.resolve_event(self.event_choice, data)
        elif action == "next_day":
            pass 
    
    def resolve_event(self, event, choice):
        """Resolve an event based on player choice"""
        outcome = event.get_outcome(choice)
        
        for effect in outcome["effects"]:
            effect_type = effect["type"]
            value = effect["value"]
            target = effect.get("target", None)
            
            if effect_type == "food":
                self.food = max(0, self.food + value)
            elif effect_type == "water":
                self.water = max(0, self.water + value)
            elif effect_type == "medical":
                self.medical = max(0, self.medical + value)
            elif effect_type == "weapons":
                self.weapons = max(0, self.weapons + value)
            elif effect_type == "tools":
                self.tools = max(0, self.tools + value)
            elif effect_type == "misc":
                self.misc = max(0, self.misc + value)
            elif effect_type == "health":
                if target == "all":
                    for member in self.family:
                        if member.is_alive:
                            member.health = max(0, min(MAX_HEALTH, member.health + value))
                elif target:
                    for member in self.family:
                        if member.name.lower() == target.lower() and member.is_alive:
                            member.health = max(0, min(MAX_HEALTH, member.health + value))
            elif effect_type == "sanity":
                if target == "all":
                    for member in self.family:
                        if member.is_alive:
                            member.sanity = max(0, min(MAX_SANITY, member.sanity + value))
                elif target:
                    for member in self.family:
                        if member.name.lower() == target.lower() and member.is_alive:
                            member.sanity = max(0, min(MAX_SANITY, member.sanity + value))
        
        if event in self.current_events:
            self.current_events.remove(event)
            self.resolved_events.append(event)
        
        self.active_panel = "main"
    
    def generate_new_events(self):
        """Generate new random events for the day"""
        new_events = self.event_manager.get_random_events(
            self.current_day,
            len([member for member in self.family if member.is_alive]),
            self.food,
            self.water,
            self.weapons,
            self.tools
        )
        
        self.current_events.extend(new_events)
    
    def process_day(self):
        """Process a day in the survival phase, return whether family survived"""
        alive_members = [member for member in self.family if member.is_alive]
        if not alive_members:
            return {
                "survived": False,
                "reason": "Cała rodzina zmarła. Koniec gry."
            }
        
        food_per_person = min(self.food, 1)  
        water_per_person = min(self.water, 1)  
        
        self.food -= food_per_person * len(alive_members)
        self.water -= water_per_person * len(alive_members)
        
        for member in alive_members:
            member.update_stats(food_per_person, water_per_person)
            
            if not member.is_alive:
                return {
                    "survived": False,
                    "reason": f"{member.name} nie żyje. Koniec gry."
                }
        self.generate_new_events()
        
        self.current_day += 1
        
        return {
            "survived": True,
            "reason": ""
        }
    
    def update(self):
        """Update the survival phase state"""
        self.buttons = []
        
        if self.active_panel == "main":
            y_pos = 80
            for i, member in enumerate(self.family):
                if member.is_alive:
                    self.buttons.append({
                        "rect": pygame.Rect(50 + i * 150, y_pos, 120, 40),
                        "text": member.name,
                        "action": "view_character",
                        "data": member
                    })
            
            y_pos = 200
            for i, event in enumerate(self.current_events[:3]): 
                self.buttons.append({
                    "rect": pygame.Rect(50, y_pos + i * 70, 250, 60),
                    "text": event.title,
                    "action": "view_event",
                    "data": event
                })
            
            inventory_text = "Ekwipunek"
            self.buttons.append({
                "rect": pygame.Rect(WIDTH - 200, 80, 150, 40),
                "text": inventory_text,
                "action": "view_inventory"
            })
            
            next_day_text = "Następny Dzień"
            self.buttons.append({
                "rect": pygame.Rect(WIDTH//2 - 75, HEIGHT - 80, 150, 50),
                "text": next_day_text,
                "action": "next_day"
            })
            
        elif self.active_panel == "character" and self.selected_character:
            back_text = "Powrót"
            self.buttons.append({
                "rect": pygame.Rect(50, 50, 100, 40),
                "text": back_text,
                "action": "back_to_main"
            })
            
            food_text = f"Daj Jedzenie ({self.food})"
            self.buttons.append({
                "rect": pygame.Rect(WIDTH - 250, 150, 200, 40),
                "text": food_text,
                "action": "consume_food"
            })
            
            water_text = f"Daj Wodę ({self.water})"
            self.buttons.append({
                "rect": pygame.Rect(WIDTH - 250, 200, 200, 40),
                "text": water_text,
                "action": "consume_water"
            })
            
            medical_text = f"Lecz ({self.medical})"
            self.buttons.append({
                "rect": pygame.Rect(WIDTH - 250, 250, 200, 40),
                "text": medical_text,
                "action": "use_medical"
            })
            
        elif self.active_panel == "event" and self.event_choice:
            back_text = "Powrót"
            self.buttons.append({
                "rect": pygame.Rect(50, 50, 100, 40),
                "text": back_text,
                "action": "back_to_main"
            })
            
            choices = self.event_choice.choices
            y_pos = HEIGHT - 200
            for i, choice in enumerate(choices):
                choice_text = choice["text"]
                if "Investigate" in choice_text:
                    choice_text = choice_text.replace("Investigate", "Zbadaj")
                elif "Ignore" in choice_text:
                    choice_text = choice_text.replace("Ignore", "Zignoruj")
                elif "Close" in choice_text:
                    choice_text = choice_text.replace("Close", "Zamknij")
                elif "Keep" in choice_text:
                    choice_text = choice_text.replace("Keep", "Utrzymaj")
                
                self.buttons.append({
                    "rect": pygame.Rect(WIDTH//2 - 150, y_pos + i * 60, 300, 50),
                    "text": choice_text,
                    "action": "resolve_event",
                    "data": i
                })
                
        elif self.active_panel == "inventory":
            back_text = "Powrót"
            self.buttons.append({
                "rect": pygame.Rect(50, 50, 100, 40),
                "text": back_text,
                "action": "back_to_main"
            })
    
    def render(self, screen, days_survived):
        """Render the survival phase UI"""
        screen.fill(DARK_GRAY)
        
        shelter_rect = pygame.Rect(WIDTH//8, HEIGHT//8, WIDTH*3//4, HEIGHT*3//4)
        pygame.draw.rect(screen, DARK_BROWN, shelter_rect)
        pygame.draw.rect(screen, BLACK, shelter_rect, 3) 
        
        font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        day_text = font_large.render(f"Day {days_survived}", True, WHITE)
        day_rect = day_text.get_rect(center=(WIDTH//2, 40))
        screen.blit(day_text, day_rect)
        
        if self.active_panel == "main":
            self.render_main_panel(screen)
        elif self.active_panel == "character" and self.selected_character:
            self.render_character_panel(screen)
        elif self.active_panel == "event" and self.event_choice:
            self.render_event_panel(screen)
        elif self.active_panel == "inventory":
            self.render_inventory_panel(screen)
        
        font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        for button in self.buttons:
            color = GRAY
            if "action" in button and button["action"] == "next_day":
                color = GREEN
            elif "action" in button and "back" in button["action"]:
                color = LIGHT_GRAY
                
            pygame.draw.rect(screen, color, button["rect"])
            pygame.draw.rect(screen, BLACK, button["rect"], 2) 
            
            if "text" in button:
                text_surface = font_medium.render(button["text"], True, BLACK)
                text_rect = text_surface.get_rect(center=button["rect"].center)
                screen.blit(text_surface, text_rect)
    
    def render_main_panel(self, screen):
        """Render the main panel showing family overview and events"""
        font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        
        status_text = font_medium.render("Status Rodziny:", True, WHITE)
        screen.blit(status_text, (70, 30))
        
        resource_x = WIDTH - 280
        resource_text = font_medium.render("Zasoby:", True, WHITE)
        screen.blit(resource_text, (resource_x, 30))
        
        resources = [
            f"Jedzenie: {self.food}",
            f"Woda: {self.water}",
            f"Medykamenty: {self.medical}",
            f"Broń: {self.weapons}",
            f"Narzędzia: {self.tools}"
        ]
        
        for i, resource in enumerate(resources):
            text = font_small.render(resource, True, WHITE)
            screen.blit(text, (resource_x, 70 + i * 25))
        
        if self.current_events:
            events_text = font_medium.render("Wydarzenia:", True, WHITE)
            screen.blit(events_text, (50, 160))
        else:
            no_events_text = font_medium.render("Brak wydarzeń dzisiaj.", True, WHITE)
            screen.blit(no_events_text, (50, 200))
    
    def render_character_panel(self, screen):
        """Render the character details panel"""
        font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        
        name_text = font_large.render(self.selected_character.name, True, WHITE)
        screen.blit(name_text, (50, 100))
        
        health_label = font_medium.render("Zdrowie:", True, WHITE)
        screen.blit(health_label, (50, 150))
        
        health_bar_rect = pygame.Rect(50, 185, 200, 20)
        pygame.draw.rect(screen, RED, health_bar_rect)
        health_fill_rect = pygame.Rect(50, 185, 200 * (self.selected_character.health / MAX_HEALTH), 20)
        pygame.draw.rect(screen, GREEN, health_fill_rect)
        
        health_text = font_small.render(f"{self.selected_character.health}/{MAX_HEALTH}", True, WHITE)
        screen.blit(health_text, (260, 185))
        
        sanity_label = font_medium.render("Psychika:", True, WHITE)
        screen.blit(sanity_label, (50, 220))
        
        sanity_bar_rect = pygame.Rect(50, 255, 200, 20)
        pygame.draw.rect(screen, RED, sanity_bar_rect)
        sanity_fill_rect = pygame.Rect(50, 255, 200 * (self.selected_character.sanity / MAX_SANITY), 20)
        pygame.draw.rect(screen, BLUE, sanity_fill_rect)
        
        sanity_text = font_small.render(f"{self.selected_character.sanity}/{MAX_SANITY}", True, WHITE)
        screen.blit(sanity_text, (260, 255))
        
        hunger_text = font_medium.render(f"Głód: {self.selected_character.hunger}%", True, WHITE)
        screen.blit(hunger_text, (50, 290))
        
        thirst_text = font_medium.render(f"Pragnienie: {self.selected_character.thirst}%", True, WHITE)
        screen.blit(thirst_text, (50, 325))
        
        status_label = font_medium.render("Stan:", True, WHITE)
        screen.blit(status_label, (50, 370))
        
        status_summary = self.selected_character.status_summary()
        for i, status in enumerate(status_summary):
            status_text = font_small.render(status, True, WHITE)
            screen.blit(status_text, (50, 405 + i * 25))
    
    def render_event_panel(self, screen):
        """Render the event details panel"""
        font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        
        title_text = font_large.render(self.event_choice.title, True, WHITE)
        screen.blit(title_text, (50, 100))
        
        description_lines = self.wrap_text(self.event_choice.description, font_medium, WIDTH - 100)
        for i, line in enumerate(description_lines):
            text = font_medium.render(line, True, LIGHT_GRAY)
            screen.blit(text, (50, 150 + i * 30))
        
        instruction_text = font_small.render("Wybierz swoje działanie:", True, WHITE)
        screen.blit(instruction_text, (50, HEIGHT - 230))
    
    def render_inventory_panel(self, screen):
        """Render the inventory panel"""
        font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        
        title_text = font_medium.render("Zapasy", True, WHITE)
        screen.blit(title_text, (50, 100))
        
        inventory_items = [
            {"name": "Jedzenie", "count": self.food, "color": GREEN},
            {"name": "Woda", "count": self.water, "color": BLUE},
            {"name": "Medykamenty", "count": self.medical, "color": WHITE},
            {"name": "Broń", "count": self.weapons, "color": RED},
            {"name": "Narzędzia", "count": self.tools, "color": ORANGE},
            {"name": "Różne", "count": self.misc, "color": YELLOW}
        ]
        
        for i, item in enumerate(inventory_items):
            pygame.draw.rect(screen, item["color"], pygame.Rect(50, 150 + i * 50, 30, 30))
            
            item_text = font_medium.render(f"{item['name']}: {item['count']}", True, WHITE)
            screen.blit(item_text, (100, 155 + i * 50))
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a given width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line_width = font.size(' '.join(current_line))[0]
            if line_width > max_width:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = MENU
        self.prev_state = None
        
        self.ui = UI()
        
        self.player = Player()
        self.inventory = Inventory()
        
        self.scavenging_phase = ScavengingPhase(self.player, self.inventory)
        self.survival_phase = SurvivalPhase(self.inventory)
        
        self.days_survived = 0
        self.game_over_reason = ""
    
        self.scavenging_timer = SCAVENGING_TIME
        self.last_timer_update = 0
        
        self.paused = False
        self.game_initialized = False
    
    def handle_event(self, event):
        """Handle pygame events based on game state"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state in [SCAVENGING, SURVIVAL]:
                    self.toggle_pause()
                    
        ui_action = self.ui.handle_event(event)
        
        if ui_action:
            self.process_ui_action(ui_action)
            
        if self.state == SCAVENGING and not self.paused:
            self.scavenging_phase.handle_event(event)
        elif self.state == SURVIVAL and not self.paused:
            survival_action = self.survival_phase.handle_event(event)
            if survival_action == "next_day":
                self.advance_day()
    
    def process_ui_action(self, action):
        """Process UI button actions"""
        if action == "start_game":
            self.start_new_game()
        elif action == "resume":
            self.toggle_pause()
        elif action == "main_menu":
            self.state = MENU
            self.paused = False
        elif action == "quit":
            pygame.quit()
            exit()
        elif action == "next_day" and self.state == SURVIVAL:
            self.advance_day()
    
    def start_new_game(self):
        """Start a new game"""
        self.player = Player()
        self.inventory = Inventory()
        self.scavenging_phase = ScavengingPhase(self.player, self.inventory)
        self.survival_phase = SurvivalPhase(self.inventory)
        self.days_survived = 0
        self.state = SCAVENGING
        self.scavenging_timer = SCAVENGING_TIME
        self.last_timer_update = time.time()
        self.game_initialized = True
    
    def toggle_pause(self):
        """Toggle game pause state"""
        self.paused = not self.paused
        if self.paused:
            self.prev_state = self.state
            self.state = PAUSE
        else:
            self.state = self.prev_state
    
    def update_scavenging_timer(self):
        """Update the timer for scavenging phase"""
        current_time = time.time()
        if current_time - self.last_timer_update >= 1:
            self.scavenging_timer -= 1
            self.last_timer_update = current_time
               
        if self.scavenging_timer <= 0:
            self.end_scavenging_phase()
    
    def end_scavenging_phase(self):
        """End scavenging phase and transition to survival"""
        self.state = SURVIVAL
        self.survival_phase.initialize(self.inventory.get_items())
    
    def advance_day(self):
        """Advance to the next day in survival phase"""
        self.days_survived += 1
        
        if self.days_survived >= DAYS_TO_WIN:
            self.game_over_reason = "Przetrwałeś wszystkie 30 dni! Wygrałeś!"
            self.state = GAME_OVER
            return
            
        survival_result = self.survival_phase.process_day()
        
        if not survival_result["survived"]:
            reason = survival_result["reason"]
            if "entire family has died" in reason:
                self.game_over_reason = "Cała rodzina zmarła. Koniec gry."
            elif "has died" in reason:
                name = reason.split(" ")[0]
                self.game_over_reason = f"{name} nie żyje. Koniec gry."
            else:
                self.game_over_reason = reason
            self.state = GAME_OVER
    
    def update(self):
        """Update game logic based on current state"""
        if self.state == MENU:
            pass
        elif self.state == SCAVENGING and not self.paused:
            self.scavenging_phase.update()
            self.update_scavenging_timer()
        elif self.state == SURVIVAL and not self.paused:
            self.survival_phase.update()
    
    def render(self, screen):
        """Render the game based on current state"""
        screen.fill(BLACK)  
        
        if self.state == MENU:
            self.ui.render_menu(screen)
        elif self.state == SCAVENGING:
            self.scavenging_phase.render(screen)
            self.ui.render_scavenging_ui(screen, self.scavenging_timer, self.inventory)
            if self.paused:
                self.ui.render_pause_menu(screen)
        elif self.state == SURVIVAL:
            self.survival_phase.render(screen, self.days_survived)
            if self.paused:
                self.ui.render_pause_menu(screen)
        elif self.state == GAME_OVER:
            self.ui.render_game_over(screen, self.days_survived, self.game_over_reason)
        elif self.state == PAUSE:
            if self.prev_state == SCAVENGING:
                self.scavenging_phase.render(screen)
                self.ui.render_scavenging_ui(screen, self.scavenging_timer, self.inventory)
            elif self.prev_state == SURVIVAL:
                self.survival_phase.render(screen, self.days_survived)
            self.ui.render_pause_menu(screen)

def main():
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    game = Game(screen)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
            
        game.update()
        
        game.render(screen)
        
        pygame.display.flip()
        
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()