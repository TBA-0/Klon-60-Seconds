import pygame
from settings import *

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
        self.init_fonts()
    
    def init_fonts(self):
        """Initialize fonts"""
        try:
            self.font_small = pygame.font.Font(f"{FONTS_DIR}/font.ttf", FONT_SIZE_SMALL)
            self.font_medium = pygame.font.Font(f"{FONTS_DIR}/font.ttf", FONT_SIZE_MEDIUM)
            self.font_large = pygame.font.Font(f"{FONTS_DIR}/font.ttf", FONT_SIZE_LARGE)
        except:
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
        
        title_text = self.font_large.render("60 SECONDS CLONE", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(title_text, title_rect)
        
        subtitle_text = self.font_medium.render("A Python/Pygame remake", True, LIGHT_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 60))
        screen.blit(subtitle_text, subtitle_rect)
        
        start_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT//2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Start Game"
        ).set_action("start_game")
        
        quit_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT//2 + BUTTON_HEIGHT + 20,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Quit"
        ).set_action("quit")
        
        self.buttons.extend([start_button, quit_button])
        
        for button in self.buttons:
            button.render(screen)

        instructions = [
            "In 60 SECONDS, you must:",
            "1. Scavenge supplies from your house in 60 seconds",
            "2. Survive in your shelter as long as possible",
            "Use WASD or Arrow Keys to move",
            "Press SPACE to pick up/drop items"
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
        
        pause_text = self.font_large.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(pause_text, pause_rect)
        
        resume_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT//2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Resume"
        ).set_action("resume")
        
        menu_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT//2 + BUTTON_HEIGHT + 20,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Main Menu"
        ).set_action("main_menu")
        
        quit_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT//2 + (BUTTON_HEIGHT + 20) * 2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Quit"
        ).set_action("quit")
        
        self.buttons.extend([resume_button, menu_button, quit_button])
        
        for button in self.buttons:
            button.render(screen)
    
    def render_scavenging_ui(self, screen, time_left, inventory):
        """Render UI elements for the scavenging phase"""
        time_text = self.font_large.render(f"{time_left}", True, WHITE if time_left > 10 else RED)
        time_rect = time_text.get_rect(topright=(WIDTH - UI_PADDING, UI_PADDING))
        screen.blit(time_text, time_rect)

        timer_label = self.font_small.render("SECONDS REMAINING", True, WHITE)
        timer_label_rect = timer_label.get_rect(topright=(WIDTH - UI_PADDING, UI_PADDING + time_rect.height))
        screen.blit(timer_label, timer_label_rect)
        
        inventory_text = self.font_medium.render(f"Items: {len(inventory.items)}/{inventory.max_items}", True, WHITE)
        inventory_rect = inventory_text.get_rect(topleft=(UI_PADDING, UI_PADDING))
        screen.blit(inventory_text, inventory_rect)
        
        controls_text = self.font_small.render("WASD/Arrows: Move   SPACE: Pick up/Drop", True, WHITE)
        controls_rect = controls_text.get_rect(midbottom=(WIDTH//2, HEIGHT - UI_PADDING))
        screen.blit(controls_text, controls_rect)

    def render_game_over(self, screen, days_survived, reason):
        """Render game over screen"""
        self.buttons = []
        screen.fill(DARK_GRAY)
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(game_over_text, game_over_rect)

        days_text = self.font_medium.render(f"Days Survived: {days_survived}", True, WHITE)
        days_rect = days_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 80))
        screen.blit(days_text, days_rect)

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

        restart_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT * 3//4,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "New Game"
        ).set_action("start_game")
        
        menu_button = Button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT * 3//4 + BUTTON_HEIGHT + 20,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Main Menu"
        ).set_action("main_menu")
        
        self.buttons.extend([restart_button, menu_button])

        for button in self.buttons:
            button.render(screen)
