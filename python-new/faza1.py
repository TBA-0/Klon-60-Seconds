import subprocess
import pygame
import random
import json
import os

# --- Ustawienia gry ---
MAP_SIZE = 5
TILE_SIZE = 64
SCREEN_SIZE = MAP_SIZE * TILE_SIZE
INVENTORY_SIZE = 4
RESOURCES = ["Drewno", "Kamień", "Żelazo", "Złoto"]

# Kolory
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 100))
pygame.display.set_caption("Zbieracz zasobów")
font = pygame.font.SysFont(None, 24)

def create_map():
    game_map = [['' for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    for _ in range(8):
        x, y = random.randint(0, MAP_SIZE - 1), random.randint(0, MAP_SIZE - 1)
        game_map[y][x] = random.choice(RESOURCES)
    return game_map

def draw_map(game_map, player_pos):
    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)
            if game_map[y][x] != '':
                text = font.render(game_map[y][x][0], True, GREEN)
                screen.blit(text, (x * TILE_SIZE + 20, y * TILE_SIZE + 20))
    px, py = player_pos
    pygame.draw.rect(screen, BLUE, (px * TILE_SIZE, py * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

def draw_inventory(inventory):
    text = font.render(f"Ekwipunek ({len(inventory)}/{INVENTORY_SIZE}): {', '.join(inventory)}", True, BLACK)
    screen.blit(text, (10, SCREEN_SIZE + 10))

def save_game(player_pos, game_map, inventory):
    data = {
        "player_pos": player_pos,
        "map": game_map,
        "inventory": inventory
    }
    with open("savegame.json", "w") as f:
        json.dump(data, f)
    print("Gra zapisana.")

def load_game():
    if os.path.exists("savegame.json"):
        with open("savegame.json", "r") as f:
            data = json.load(f)
        print("Gra wczytana.")
        return list(map(int, data["player_pos"])), data["map"], data["inventory"]
    else:
        print("Brak zapisu gry. Tworzenie nowego...")
        player_pos = [0, 0]
        game_map = create_map()
        inventory = []
        save_game(player_pos, game_map, inventory)
        return player_pos, game_map, inventory

def main():
    clock = pygame.time.Clock()
    running = True

    player_pos, game_map, inventory = load_game()
    move_count = 0
    key_cooldown = 0  # blokada na nadmiarowe naciśnięcia

    while running:
        screen.fill(WHITE)
        draw_map(game_map, player_pos)
        draw_inventory(inventory)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        moved = False

        if key_cooldown == 0:
            if keys[pygame.K_UP] and player_pos[1] > 0:
                player_pos[1] -= 1
                moved = True
            elif keys[pygame.K_DOWN] and player_pos[1] < MAP_SIZE - 1:
                player_pos[1] += 1
                moved = True
            elif keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= 1
                moved = True
            elif keys[pygame.K_RIGHT] and player_pos[0] < MAP_SIZE - 1:
                player_pos[0] += 1
                moved = True

            if moved:
                move_count += 1
                print(f"Ruch {move_count}/5")
                key_cooldown = 10  # blokada przez kilka klatek

            elif keys[pygame.K_SPACE]:
                x, y = player_pos
                item = game_map[y][x]
                if item != '' and len(inventory) < INVENTORY_SIZE:
                    inventory.append(item)
                    game_map[y][x] = ''
                elif item == '':
                    print("Tutaj nic nie ma.")
                else:
                    print("Ekwipunek pełny.")
                key_cooldown = 10

            elif keys[pygame.K_z]:
                save_game(player_pos, game_map, inventory)
                key_cooldown = 10

            elif keys[pygame.K_w]:
                player_pos, game_map, inventory = load_game()
                key_cooldown = 10

        if move_count >= 5:
            print("Osiągnięto limit ruchów. Przechodzenie do fazy 2...")
            pygame.quit()
            subprocess.run(["python", "python-new/faza2.py"])
            return

        if key_cooldown > 0:
            key_cooldown -= 1

        clock.tick(30)

if __name__ == "__main__":
    main()
