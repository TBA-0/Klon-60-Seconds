import pygame
import random
from settings import *
from items import ItemFactory

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
