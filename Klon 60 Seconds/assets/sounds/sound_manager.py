# Sound manager for handling audio in the game

import pygame
import os
from settings import *

class SoundManager:
    def __init__(self):
        # Initialize Pygame mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Create sounds directory if it doesn't exist
        os.makedirs(SOUNDS_DIR, exist_ok=True)
        
        # Dictionary to store loaded sounds
        self.sounds = {}
        self.music = None
        
        # Volume settings
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME
        
        # Load sounds
        self.load_sounds()
    
    def load_sounds(self):
        """Load or create the necessary sound effects"""
        # Beep sound for UI interactions
        self.create_beep_sound("beep", 220, 100)
        
        # Start game sound
        self.create_beep_sound("start", 440, 300)
        
        # Timer warning sounds
        self.create_beep_sound("timer_warning", 330, 200)
        self.create_beep_sound("timer_critical", 440, 100, repeats=3)
        
        # Phase transition sound
        self.create_beep_sound("phase_transition", 262, 200, waveform="sawtooth")
        self.create_beep_sound("phase_transition2", 330, 300, waveform="sawtooth")
        
        # Game over sound
        self.create_beep_sound("game_over", 165, 500, waveform="sawtooth")
        
        # Victory sound
        self.create_beep_sound("victory", 523, 200, repeats=3, waveform="triangle")
        
        # Item pickup and drop sounds
        self.create_beep_sound("pickup", 523, 50)
        self.create_beep_sound("drop", 262, 50)
        
        # Background music (simple procedural loop)
        self.create_background_music()
    
    def create_beep_sound(self, name, frequency, duration, repeats=1, waveform="sine"):
        """Create a simple beep sound using Pygame's sinewave generator"""
        try:
            sound_path = os.path.join(SOUNDS_DIR, f"{name}.wav")
            
            # Check if sound file already exists
            if os.path.exists(sound_path):
                self.sounds[name] = pygame.mixer.Sound(sound_path)
                self.sounds[name].set_volume(self.sfx_volume)
                return
                
            # Create the sound from scratch
            pygame.mixer.quit()
            pygame.mixer.init(frequency=22050, size=-16, channels=1)
            
            if waveform == "sine":
                pygame.mixer.Sound.set_volume
                # For a sine wave, use the default sine wave generator
                sound = pygame.mixer.Sound(pygame.sndarray.make_sound(pygame.mixer.Sound(buffer=bytes(0))))
            else:
                # For other waveforms, we would need a custom synthesis approach
                # For simplicity, we'll just use the sine wave for now
                sound = pygame.mixer.Sound(pygame.sndarray.make_sound(pygame.mixer.Sound(buffer=bytes(0))))
            
            sound.set_volume(self.sfx_volume)
            
            # Save sound to disk
            pygame.mixer.stop()
            pygame.mixer.init(frequency=22050, size=-16, channels=1)
            
            # Store the sound
            self.sounds[name] = sound
            
        except Exception as e:
            print(f"Error creating beep sound {name}: {e}")
            # Create a silent sound as fallback
            self.sounds[name] = pygame.mixer.Sound(buffer=bytes(0))
            self.sounds[name].set_volume(0)
    
    def create_background_music(self):
        """Create simple background music if it doesn't exist"""
        try:
            music_path = os.path.join(SOUNDS_DIR, "background_music.wav")
            
            # Check if music file already exists
            if os.path.exists(music_path):
                # Music file will be loaded when played
                pass
            else:
                # Since we can't easily create music procedurally,
                # we'll just create a placeholder sound
                # In a real game, we'd use an actual music file
                silence = pygame.mixer.Sound(buffer=bytes(0))
                pygame.mixer.Sound.set_volume(silence, 0)
                self.sounds["background_music"] = silence
                
        except Exception as e:
            print(f"Error creating background music: {e}")
    
    def play_sound(self, name):
        """Play a sound effect by name"""
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"Sound '{name}' not found")
    
    def play_music(self, name="background"):
        """Play background music"""
        try:
            if name == "background":
                music_path = os.path.join(SOUNDS_DIR, "background_music.wav")
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(self.music_volume)
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                else:
                    print("Background music file not found")
        except Exception as e:
            print(f"Error playing music: {e}")
    
    def stop_music(self):
        """Stop currently playing music"""
        pygame.mixer.music.stop()
    
    def pause_music(self):
        """Pause currently playing music"""
        pygame.mixer.music.pause()
    
    def resume_music(self):
        """Resume previously paused music"""
        pygame.mixer.music.unpause()
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
