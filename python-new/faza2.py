import pygame
import sys
import json
import os
import random
import time

import settings

user_settings = settings.load_settings()




pygame.init()

if user_settings["fullscreen"]:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
else:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Faza 2 - Interfejs postapokaliptyczny")
font = pygame.font.SysFont("arial", 20)
clock = pygame.time.Clock()

background = None
if user_settings["background"]:
    try:
        background = pygame.image.load(user_settings["background"])
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        background = None

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
BLUE = (100, 100, 255)
RED = (200, 50, 50)
GREEN = (50, 200, 50)

tabs = ["questy", "polityka", "ulepszenia", "ekwipunek", "frakcje", "ustawienia"]
active_tab = "questy"
setting_buttons = {
    "fullscreen": pygame.Rect(70, 100, 300, 30),
    "volume": pygame.Rect(70, 140, 300, 30),
    "backgrounds": []  # lista z przyciskami tła
}

def draw_button(text, rect, color=GRAY):
    pygame.draw.rect(screen, color, rect)
    draw_text(text, rect.x + 10, rect.y + 5)



def draw_settings_tab():
    draw_text("USTAWIENIA:", 50, 50)

    # Pełny ekran
    fs_text = f"Pełny ekran: {'TAK' if user_settings['fullscreen'] else 'NIE'}"
    draw_button(fs_text, setting_buttons["fullscreen"])

    # Głośność
    vol_text = f"Głośność: {int(user_settings['volume'] * 100)}%"
    draw_button(vol_text, setting_buttons["volume"])

    # Lista teł
    draw_text("Wybierz tło:", 70, 190)
    setting_buttons["backgrounds"] = []
    files = [f for f in os.listdir("python-new/backgrounds") if f.endswith((".png", ".jpg"))]
    for i, name in enumerate(files[:3]):
        rect = pygame.Rect(100, 220 + i * 40, 300, 30)
        setting_buttons["backgrounds"].append((rect, name))
        draw_button(f"Tło: {name}", rect)


if active_tab == "ustawienia":
    draw_settings_tab()

inventory_items = json.load(open("savegame.json")).get("inventory", []) if os.path.exists("savegame.json") else []
stats = {
    "Zdrowie": 85,
    "Stres": 30,
    "Wiek": 5,
    "EXP": 210,
    "Szaleństwo": 0,
    "Ścieżka": "neutralna"
}
factions = {
    "Milicja": 40,
    "Technokraci": 60,
    "Zakon Węgla": 20,
    "Obywatele": 55
}
upgrades = []
upgrade_options = ["Filtr wody", "Lepszy schron", "Mapa tuneli", "Kontakt z frakcją"]

current_moral_choice = None
moral_choices_this_day = 0
current_day = 1
day_timer = 300  # 5 minut
start_time = time.time()
waiting_for_next_day = False

def generate_moral_choice():
    options = [
        {
            "desc": "Znajdujesz głodnego dziecka. Czy dzielisz się zapasami?",
            "choices": [("Tak (Stres -10, Szaleństwo -5)", {"Stres": -10, "Szaleństwo": -5}),
                        ("Nie (Szaleństwo +10)", {"Szaleństwo": 10})]
        },
        {
            "desc": "Frakcja Milicji prosi o pomoc w zasadzce. Czy pomagasz?",
            "choices": [("Tak (Milicja +15, EXP +30)", {"Milicja": 15, "EXP": 30}),
                        ("Nie (Milicja -10, Szaleństwo +5)", {"Milicja": -10, "Szaleństwo": 5})]
        },
        {
            "desc": "Masz okazję ukraść zapasy Technokratów.",
            "choices": [("Ukradnij (EXP +20, Technokraci -20)", {"EXP": 20, "Technokraci": -20}),
                        ("Zostaw (Szaleństwo -5)", {"Szaleństwo": -5})]
        },
    ]
    return random.choice(options)

def draw_text(text, x, y, color=BLACK, center=False):
    txt_surface = font.render(text, True, color)
    rect = txt_surface.get_rect(center=(x, y)) if center else (x, y)
    screen.blit(txt_surface, rect)

def draw_tabs():
    for i, name in enumerate(tabs):
        color = DARK_GRAY if active_tab == name else GRAY
        rect = pygame.Rect(10, 280 + i * 40, 280, 30)
        pygame.draw.rect(screen, color, rect)
        draw_text(name, 20, 285 + i * 40)

def draw_inventory():
    draw_text("Ekwipunek:", 320, 50)
    for i, item in enumerate(inventory_items):
        draw_text(f"- {item}", 340, 80 + i * 30)

def draw_stats():
    y = 500
    draw_text("Statystyki:", 10, y)
    for i, (k, v) in enumerate(stats.items()):
        draw_text(f"{k}: {v}%", 20, y + 25 + i * 20)

def draw_factions():
    draw_text("Relacje z frakcjami:", 320, 50)
    for i, (faction, support) in enumerate(factions.items()):
        draw_text(f"{faction}: {support}%", 340, 80 + i * 30)

def draw_upgrades():
    draw_text("Ulepszenia:", 320, 50)
    for i, name in enumerate(upgrades):
        draw_text(f"- {name}", 340, 80 + i * 30)
    draw_text("Kliknij [U] by dodać losowe ulepszenie", 320, 300, RED)

def draw_quests():
    draw_text("Aktualne zadania:", 320, 50)
    draw_text("M - quest główny 1", 340, 80)
    for i in range(4):
        draw_text(f"S - sidequest {i+1}", 340, 110 + i * 30)

def draw_moral_choice():
    if not current_moral_choice:
        return
    draw_text("Wybór moralny:", 900, 500)
    draw_text(current_moral_choice["desc"], 900, 530)
    for i, (text, _) in enumerate(current_moral_choice["choices"]):
        draw_text(f"{i + 1}. {text}", 900, 560 + i * 25)

def apply_choice(index):
    global current_moral_choice, moral_choices_this_day, waiting_for_next_day
    if current_moral_choice:
        effects = current_moral_choice["choices"][index][1]
        for k, v in effects.items():
            if k in stats:
                stats[k] += v
            elif k in factions:
                factions[k] += v
        moral_choices_this_day += 1
        current_moral_choice = None
        if moral_choices_this_day >= 3:
            waiting_for_next_day = True

def draw_day_info():
    draw_text(f"Dzień: {current_day}", SCREEN_WIDTH - 150, 10)
    remaining = max(0, int(day_timer - (time.time() - start_time)))
    draw_text(f"Czas do zmroku: {remaining}s", SCREEN_WIDTH - 200, 40)

def prompt_next_day():
    draw_text("Dzień się kończy. Przejść do kolejnego?", 400, 600, RED)
    draw_text("Naciśnij [Enter], aby przejść dalej", 400, 630, RED)

def reset_day():
    global start_time, moral_choices_this_day, current_day, current_moral_choice, waiting_for_next_day
    current_day += 1
    start_time = time.time()
    moral_choices_this_day = 0
    current_moral_choice = generate_moral_choice()
    waiting_for_next_day = False

def draw_middle_section():
    if active_tab == "ekwipunek":
        draw_inventory()
    elif active_tab == "questy":
        draw_quests()
    elif active_tab == "ulepszenia":
        draw_upgrades()
    elif active_tab == "polityka":
        draw_text("System polityczny - wybierz drogę...", 320, 50)
    elif active_tab == "frakcje":
        draw_factions()

def draw_ui():
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill((255, 255, 255))  # domyślne białe tło
    pygame.draw.rect(screen, GRAY, (0, 0, 300, SCREEN_HEIGHT))
    draw_text("Zakładki menu", 10, 10)
    draw_tabs()
    draw_text("info o wersji / twórcach", 10, SCREEN_HEIGHT - 30)
    draw_middle_section()
    draw_stats()
    draw_moral_choice()
    draw_day_info()
    if waiting_for_next_day:
        prompt_next_day()

def get_tab_clicked(pos):
    x, y = pos
    if 10 <= x <= 290:
        for i, name in enumerate(tabs):
            if 280 + i * 40 <= y <= 280 + i * 40 + 30:
                return name
    return None

def main():
    global active_tab, current_moral_choice, waiting_for_next_day, background

    current_moral_choice = generate_moral_choice()

    while True:
        draw_ui()

        # Jeśli aktywna zakładka to "ustawienia", rysujemy przyciski
        if active_tab == "ustawienia":
            draw_settings_tab()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_tab = get_tab_clicked(event.pos)
                if clicked_tab:
                    active_tab = clicked_tab  # <-- kluczowa linia!
                else:
                    if active_tab == "ustawienia":
                        mx, my = event.pos

                        # Klik: Pełny ekran
                        if setting_buttons["fullscreen"].collidepoint(mx, my):
                            user_settings["fullscreen"] = not user_settings["fullscreen"]
                            settings.save_settings(user_settings)
                            pygame.quit()
                            os.execl(sys.executable, sys.executable, *sys.argv)

                        # Klik: Głośność
                        elif setting_buttons["volume"].collidepoint(mx, my):
                            user_settings["volume"] = round((user_settings["volume"] + 0.1) % 1.1, 1)
                            pygame.mixer.music.set_volume(user_settings["volume"])
                            settings.save_settings(user_settings)

                        # Klik: wybór tła
                        for rect, name in setting_buttons["backgrounds"]:
                            if rect.collidepoint(mx, my):
                                path = os.path.join("python-new/backgrounds", name)
                                user_settings["background"] = path
                                settings.save_settings(user_settings)
                                try:
                                    background = pygame.image.load(path)
                                    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                                except:
                                    background = None

            elif event.type == pygame.KEYDOWN:
                if active_tab == "ustawienia":
                    if event.key == pygame.K_1:
                        user_settings["fullscreen"] = not user_settings["fullscreen"]
                        settings.save_settings(user_settings)
                        pygame.quit()
                        os.execl(sys.executable, sys.executable, *sys.argv)

                    elif event.key == pygame.K_2:
                        user_settings["volume"] = round((user_settings["volume"] + 0.1) % 1.1, 1)
                        pygame.mixer.music.set_volume(user_settings["volume"])
                        settings.save_settings(user_settings)

                    elif event.key in [pygame.K_3, pygame.K_4, pygame.K_5]:
                        index = event.key - pygame.K_3
                        files = [f for f in os.listdir("python-new/backgrounds") if f.endswith((".png", ".jpg"))]
                        if index < len(files):
                            path = os.path.join("python-new/backgrounds", files[index])
                            user_settings["background"] = path
                            settings.save_settings(user_settings)
                            try:
                                background = pygame.image.load(path)
                                background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                            except:
                                background = None

                # Nowy dzień
                if waiting_for_next_day and event.key == pygame.K_RETURN:
                    reset_day()

                # Moralny wybór
                if not waiting_for_next_day:
                    if current_moral_choice:
                        if event.key == pygame.K_1:
                            apply_choice(0)
                        elif event.key == pygame.K_2:
                            apply_choice(1)

                # Dodanie ulepszenia
                if event.key == pygame.K_u and active_tab == "ulepszenia":
                    new_upg = random.choice([u for u in upgrade_options if u not in upgrades])
                    upgrades.append(new_upg)

        # Zegar dnia
        if not waiting_for_next_day and time.time() - start_time >= day_timer:
            waiting_for_next_day = True

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
    
    