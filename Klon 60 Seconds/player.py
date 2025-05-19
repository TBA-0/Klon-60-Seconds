import pygame
from settings import *

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
