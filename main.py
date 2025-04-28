import pygame
import random
import json
import os
#from button import Button


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# "zasoby"/statystyki
state = {
    "gospodarka": 50,
    "wojsko": 50,
    "opinia_publiczna": 50,
    "run": 1
}

# wczytaj save'a
SAVE_FILE = "data/save.json"
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, 'r') as f:
        saved = json.load(f)
        state.update(saved)

# randomowy event
from events.event_manager import get_random_event

def draw_text(surface, text, x, y, color=(255, 255, 255)):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        img = font.render(line, True, color)
        surface.blit(img, (x, y + i * 30))

def handle_event(event_data):
    screen.fill((30, 30, 30))
    draw_text(screen, event_data["text"], 50, 50)
    y_offset = 200
    keys = list(event_data["options"].keys())
    for i, opt in enumerate(keys):
        draw_text(screen, f"{i+1}. {opt}", 70, y_offset + i * 40)
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key in [pygame.K_1, pygame.K_2]:
                    choice = keys[e.key - pygame.K_1]
                    outcome = event_data["options"][choice]
                    for key in outcome:
                        state[key] += outcome[key]
                    return

running = True
while running:
    screen.fill((0, 0, 0))

    # wybor randomowego eventu
    current_event = get_random_event()
    handle_event(current_event)

    # progres
    y = 400
    for key, val in state.items():
        draw_text(screen, f"{key}: {val}", 50, y)
        y += 30

    pygame.display.flip()
    pygame.time.delay(2000)

    # game over
    if state["gospodarka"] <= 0 or state["wojsko"] <= 0 or state["opinia_publiczna"] <= 0:
        draw_text(screen, "Upadłeś jako lider. Game Over.", 200, 300)
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

# saveowanie gry
with open(SAVE_FILE, 'w') as f:
    json.dump(state, f)

pygame.quit()