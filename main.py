import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 36)

# Kolory
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Gracz
player_size = 40
player_pos = [WIDTH // 2 - player_size // 2, HEIGHT // 2 - player_size // 2]  # Gracz na środku
player_speed = 5
inventory = []  # Przechowywanie przedmiotów

# Ściany i drzwi
walls = [
    pygame.Rect(50, 50, 700, 20),  # Górna ściana pokoju
    pygame.Rect(50, 50, 20, 700),  # Lewa ściana pokoju
    pygame.Rect(730, 50, 20, 700), # Prawa ściana pokoju
    pygame.Rect(50, 730, 700, 20), # Dolna ściana pokoju
    pygame.Rect(350, 50, 20, 200), # Ściana dzieląca pokoje
]

# Drzwi
door = pygame.Rect(350, 200, 50, 20)  # Drzwi w ścianie

# Obiekty w pokoju
objects = [
    {"name": "Woda", "rect": pygame.Rect(200, 100, 30, 30), "collected": False},
    {"name": "Jedzenie", "rect": pygame.Rect(400, 100, 30, 30), "collected": False},
    {"name": "Latarka", "rect": pygame.Rect(600, 100, 30, 30), "collected": False},
    {"name": "Karty", "rect": pygame.Rect(200, 400, 30, 30), "collected": False},
    {"name": "Telefon", "rect": pygame.Rect(400, 400, 30, 30), "collected": False},
    {"name": "Ładowarka", "rect": pygame.Rect(600, 400, 30, 30), "collected": False},
]

# Funkcja rysująca tekst
def draw_text(surface, text, x, y, color=(255, 255, 255), font_size=36):
    font = pygame.font.SysFont("arial", font_size)
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

# Funkcja rysująca przycisk
def draw_button(surface, text, x, y, width, height, color, hover_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
        pygame.draw.rect(surface, hover_color, (x, y, width, height))  # Hover effect
    else:
        pygame.draw.rect(surface, color, (x, y, width, height))  # Normal button

    draw_text(surface, text, x + 20, y + 10, WHITE)

# Funkcja menu głównego
def main_menu():
    running = True
    while running:
        screen.fill(BLACK)

        draw_text(screen, "Witaj w grze!", WIDTH // 2 - 120, HEIGHT // 4, WHITE, 48)
        
        # Rysowanie przycisków Start i Exit
        draw_button(screen, "Start", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GREEN, (0, 200, 0))
        draw_button(screen, "Exit", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, RED, (200, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Start gry
                if WIDTH // 2 - 100 <= mouse_x <= WIDTH // 2 + 100 and HEIGHT // 2 - 50 <= mouse_y <= HEIGHT // 2 + 50:
                    return "start"
                # Zakończenie gry
                elif WIDTH // 2 - 100 <= mouse_x <= WIDTH // 2 + 100 and HEIGHT // 2 + 50 <= mouse_y <= HEIGHT // 2 + 100:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

# Funkcja gry
def game_loop():
    global player_pos
    running = True
    while running:
        screen.fill(BLACK)

        # Rysowanie pokoju (ściany)
        for wall in walls:
            pygame.draw.rect(screen, (169, 169, 169), wall)

        # Rysowanie drzwi
        pygame.draw.rect(screen, YELLOW, door)

        # Rysowanie obiektów (woda, jedzenie, itd.)
        for obj in objects:
            if not obj["collected"]:
                pygame.draw.rect(screen, (0, 255, 255), obj["rect"])  # Kolor dla obiektów

        # Rysowanie gracza
        pygame.draw.rect(screen, GREEN, (player_pos[0], player_pos[1], player_size, player_size))

        # Obsługa ruchu gracza za pomocą WASD
        keys = pygame.key.get_pressed()
        new_pos = player_pos.copy()

        if keys[pygame.K_a]:  # W lewo
            new_pos[0] -= player_speed
        if keys[pygame.K_d]:  # W prawo
            new_pos[0] += player_speed
        if keys[pygame.K_w]:  # W górę
            new_pos[1] -= player_speed
        if keys[pygame.K_s]:  # W dół
            new_pos[1] += player_speed

        # Kolizje z ścianami
        player_rect = pygame.Rect(new_pos[0], new_pos[1], player_size, player_size)
        for wall in walls:
            if player_rect.colliderect(wall):
                new_pos = player_pos
                break

        # Jeśli nie ma kolizji, zaktualizuj pozycję gracza
        player_pos = new_pos

        # Sprawdzanie interakcji z drzwiami (naciśnięcie E)
        if door.collidepoint(player_pos[0] + player_size / 2, player_pos[1] + player_size / 2):
            if keys[pygame.K_e]:
                print("Gracz przeszedł przez drzwi!")
                player_pos = [WIDTH // 2 - player_size // 2, HEIGHT // 2 - player_size // 2]  # Resetowanie pozycji gracza

        # Sprawdzanie podnoszenia obiektów po kliknięciu
        for obj in objects:
            if not obj["collected"]:
                if obj["rect"].collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:  # Lewy przycisk myszy
                        obj["collected"] = True
                        inventory.append(obj["name"])
                        print(f"Podniosłeś {obj['name']}")

        # Wyświetlanie inwentarza
        draw_text(screen, "Inwentarz: " + ", ".join(inventory), 20, HEIGHT - 50, WHITE, 24)

        # Sprawdzanie wyjścia
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

# Główna funkcja
def main():
    choice = main_menu()
    if choice == "start":
        game_loop()

if __name__ == "__main__":
    main()
