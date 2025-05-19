import pygame
import random
import json
import os
from settings import *
from events import EventManager

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
            status.append("Healthy")
        elif self.health >= 50:
            status.append("Minor injuries")
        elif self.health >= 25:
            status.append("Seriously injured")
        else:
            status.append("Critical condition")

        if self.hunger <= 0:
            status.append("Starving")
        elif self.hunger <= 25:
            status.append("Very hungry")
        elif self.hunger <= 50:
            status.append("Hungry")

        if self.thirst <= 0:
            status.append("Dehydrated")
        elif self.thirst <= 25:
            status.append("Very thirsty")
        elif self.thirst <= 50:
            status.append("Thirsty")

        if self.is_sick:
            status.append("Sick")
        if self.is_injured:
            status.append("Injured")
        if self.is_insane:
            status.append("Insane")
            
        return status


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

        self.generate_new_events()
    
    def handle_event(self, event):
        """Handle events for the survival phase"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    self.process_button_action(button["action"], button.get("data"))
    
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
                "reason": "Your entire family has died. Game Over."
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
                    "reason": f"{member.name} has died. Game Over."
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
            
            self.buttons.append({
                "rect": pygame.Rect(WIDTH - 200, 80, 150, 40),
                "text": "Inventory",
                "action": "view_inventory"
            })
            
            self.buttons.append({
                "rect": pygame.Rect(WIDTH//2 - 75, HEIGHT - 80, 150, 50),
                "text": "Next Day",
                "action": "next_day"
            })

        elif self.active_panel == "character" and self.selected_character:
            self.buttons.append({
                "rect": pygame.Rect(50, 50, 100, 40),
                "text": "Back",
                "action": "back_to_main"
            })

            self.buttons.append({
                "rect": pygame.Rect(WIDTH - 250, 150, 200, 40),
                "text": f"Give Food ({self.food})",
                "action": "consume_food"
            })

            self.buttons.append({
                "rect": pygame.Rect(WIDTH - 250, 200, 200, 40),
                "text": f"Give Water ({self.water})",
                "action": "consume_water"
            })

            self.buttons.append({
                "rect": pygame.Rect(WIDTH - 250, 250, 200, 40),
                "text": f"Treat ({self.medical})",
                "action": "use_medical"
            })
            
        elif self.active_panel == "event" and self.event_choice:
            self.buttons.append({
                "rect": pygame.Rect(50, 50, 100, 40),
                "text": "Back",
                "action": "back_to_main"
            })
            
            choices = self.event_choice.choices
            y_pos = HEIGHT - 200
            for i, choice in enumerate(choices):
                self.buttons.append({
                    "rect": pygame.Rect(WIDTH//2 - 150, y_pos + i * 60, 300, 50),
                    "text": choice["text"],
                    "action": "resolve_event",
                    "data": i
                })
                
        elif self.active_panel == "inventory":
            self.buttons.append({
                "rect": pygame.Rect(50, 50, 100, 40),
                "text": "Back",
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
        elif self.active_panel == "character":
            self.render_character_panel(screen)
        elif self.active_panel == "event":
            self.render_event_panel(screen)
        elif self.active_panel == "inventory":
            self.render_inventory_panel(screen)

        font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        for button in self.buttons:
            pygame.draw.rect(screen, LIGHT_GRAY, button["rect"])
            pygame.draw.rect(screen, BLACK, button["rect"], 2)

            text = font.render(button["text"], True, BLACK)
            text_rect = text.get_rect(center=button["rect"].center)
            screen.blit(text, text_rect)
    
    def render_main_panel(self, screen):
        """Render the main panel showing family overview and events"""
        font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

        pygame.draw.rect(screen, BROWN, (30, 30, WIDTH - 60, 120))
        title_text = font.render("Family Status", True, WHITE)
        screen.blit(title_text, (50, 40))

        pygame.draw.rect(screen, BROWN, (30, 170, 300, 300))
        title_text = font.render("Events", True, WHITE)
        screen.blit(title_text, (50, 180))
        
        if not self.current_events:
            no_events_text = font_small.render("No events today", True, WHITE)
            screen.blit(no_events_text, (50, 220))

        pygame.draw.rect(screen, BROWN, (WIDTH - 250, 170, 220, 300))
        title_text = font.render("Supplies", True, WHITE)
        screen.blit(title_text, (WIDTH - 230, 180))

        resources = [
            f"Food: {self.food}",
            f"Water: {self.water}",
            f"Medical: {self.medical}",
            f"Weapons: {self.weapons}",
            f"Tools: {self.tools}",
            f"Misc items: {self.misc}"
        ]
        
        y_pos = 220
        for resource in resources:
            text = font_small.render(resource, True, WHITE)
            screen.blit(text, (WIDTH - 230, y_pos))
            y_pos += 30
    
    def render_character_panel(self, screen):
        """Render the character details panel"""
        if not self.selected_character:
            return
            
        character = self.selected_character
        font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

        name_text = font.render(character.name, True, WHITE)
        screen.blit(name_text, (200, 80))

        stats = [
            f"Health: {character.health}/{MAX_HEALTH}",
            f"Sanity: {character.sanity}/{MAX_SANITY}",
            f"Hunger: {character.hunger}/100",
            f"Thirst: {character.thirst}/100"
        ]
        
        y_pos = 130
        for stat in stats:
            text = font_small.render(stat, True, WHITE)
            screen.blit(text, (200, y_pos))
            y_pos += 30

        status = character.status_summary()
        status_text = font_small.render("Status: " + ", ".join(status), True, WHITE)
        screen.blit(status_text, (200, y_pos + 20))

        avatar_rect = pygame.Rect(50, 130, 120, 120)
        pygame.draw.rect(screen, BLUE, avatar_rect)

        bar_width = 200
        bar_height = 20
        x_pos = 300
        y_pos = 130

        health_width = int((character.health / MAX_HEALTH) * bar_width)
        pygame.draw.rect(screen, RED, (x_pos, y_pos, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (x_pos, y_pos, health_width, bar_height))

        y_pos += 30
        sanity_width = int((character.sanity / MAX_SANITY) * bar_width)
        pygame.draw.rect(screen, RED, (x_pos, y_pos, bar_width, bar_height))
        pygame.draw.rect(screen, BLUE, (x_pos, y_pos, sanity_width, bar_height))

        y_pos += 30
        hunger_width = int((character.hunger / 100) * bar_width)
        pygame.draw.rect(screen, RED, (x_pos, y_pos, bar_width, bar_height))
        pygame.draw.rect(screen, YELLOW, (x_pos, y_pos, hunger_width, bar_height))

        y_pos += 30
        thirst_width = int((character.thirst / 100) * bar_width)
        pygame.draw.rect(screen, RED, (x_pos, y_pos, bar_width, bar_height))
        pygame.draw.rect(screen, BLUE, (x_pos, y_pos, thirst_width, bar_height))
    
    def render_event_panel(self, screen):
        """Render the event details panel"""
        if not self.event_choice:
            return
            
        event = self.event_choice
        font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

        title_text = font.render(event.title, True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, 100))
        screen.blit(title_text, title_rect)

        description_lines = self.wrap_text(event.description, font_small, WIDTH - 200)
        y_pos = 150
        for line in description_lines:
            text = font_small.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH//2, y_pos))
            screen.blit(text, text_rect)
            y_pos += 25

        choices_text = font.render("Your options:", True, WHITE)
        choices_rect = choices_text.get_rect(center=(WIDTH//2, HEIGHT - 250))
        screen.blit(choices_text, choices_rect)
    
    def render_inventory_panel(self, screen):
        """Render the inventory panel"""
        font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

        title_text = font.render("Shelter Supplies", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, 100))
        screen.blit(title_text, title_rect)

        categories = [
            {"name": "Food", "count": self.food, "color": GREEN},
            {"name": "Water", "count": self.water, "color": BLUE},
            {"name": "Medical Supplies", "count": self.medical, "color": WHITE},
            {"name": "Weapons", "count": self.weapons, "color": RED},
            {"name": "Tools", "count": self.tools, "color": ORANGE},
            {"name": "Miscellaneous", "count": self.misc, "color": YELLOW}
        ]

        grid_cols = 2
        item_width = 200
        item_height = 80
        x_margin = (WIDTH - (grid_cols * item_width)) // 2
        y_start = 150
        
        for i, category in enumerate(categories):
            col = i % grid_cols
            row = i // grid_cols
            
            x = x_margin + col * item_width
            y = y_start + row * item_height

            category_rect = pygame.Rect(x, y, item_width - 20, item_height - 10)
            pygame.draw.rect(screen, DARK_GRAY, category_rect)
            pygame.draw.rect(screen, category["color"], category_rect, 2)

            name_text = font_small.render(category["name"], True, WHITE)
            screen.blit(name_text, (x + 10, y + 10))

            count_text = font.render(str(category["count"]), True, category["color"])
            screen.blit(count_text, (x + item_width - 60, y + 25))
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a given width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            width = font.size(test_line)[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
