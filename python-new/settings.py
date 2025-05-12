import json
import os

# Domyślne ustawienia gry
DEFAULTS = {
    "fullscreen": False,
    "volume": 0.5,
    "background": "tlo1.png"
}

def load_settings():
    # Wczytuje ustawienia z pliku (jeśli plik istnieje)
    if os.path.exists("user_settings.json"):
        with open("user_settings.json", "r") as file:
            return json.load(file)
    return DEFAULTS.copy()

def save_settings(data):
    # Zapisuje ustawienia do pliku
    with open("user_settings.json", "w") as file:
        json.dump(data, file, indent=4)
