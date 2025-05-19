import pygame
import time
from settings import *
from scavenging_phase import ScavengingPhase
from survival_phase import SurvivalPhase
from ui import UI
from player import Player
from items import Inventory
from assets.sounds.sound_manager import SoundManager

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = MENU
        self.prev_state = None
        
        self.ui = UI()

        self.sound_manager = SoundManager()
        self.sound_manager.play_music("background")
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
            self.survival_phase.handle_event(event)
    
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
        self.sound_manager.play_sound("start")
    
    def toggle_pause(self):
        """Toggle game pause state"""
        self.paused = not self.paused
        if self.paused:
            self.prev_state = self.state
            self.state = PAUSE
            self.sound_manager.pause_music()
        else:
            self.state = self.prev_state
            self.sound_manager.resume_music()
    
    def update_scavenging_timer(self):
        """Update the timer for scavenging phase"""
        current_time = time.time()
        if current_time - self.last_timer_update >= 1:
            self.scavenging_timer -= 1
            self.last_timer_update = current_time
            if self.scavenging_timer in [30, 20, 10]:
                self.sound_manager.play_sound("timer_warning")
            elif self.scavenging_timer <= 5:
                self.sound_manager.play_sound("timer_critical")
        if self.scavenging_timer <= 0:
            self.end_scavenging_phase()
    
    def end_scavenging_phase(self):
        """End scavenging phase and transition to survival"""
        self.state = SURVIVAL
        self.sound_manager.play_sound("phase_transition")
        self.survival_phase.initialize(self.inventory.get_items())
    
    def advance_day(self):
        """Advance to the next day in survival phase"""
        self.days_survived += 1
        if self.days_survived >= DAYS_TO_WIN:
            self.game_over_reason = "You survived all 30 days! You win!"
            self.state = GAME_OVER
            self.sound_manager.play_sound("victory")
            return
        survival_result = self.survival_phase.process_day()
        if not survival_result["survived"]:
            self.game_over_reason = survival_result["reason"]
            self.state = GAME_OVER
            self.sound_manager.play_sound("game_over")
    
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
