# Dokumentacja Gry: 60 Sekund – Klon „60 Seconds”

## Cel gry
Gracz ma 60 sekund na zebranie zapasów w domu, a następnie musi przetrwać 30 dni w schronie, zarządzając zasobami i podejmując decyzje, które wpływają na zdrowie i psychikę członków rodziny.

---

## Technologie
- **Język**: Python 3.6+
- **Biblioteki:**
  - `pygame` – silnik gry 2D
  - `numpy` – operacje na danych liczbowych
  - `json` – obsługa danych gry (przedmioty, wydarzenia)

---

## Struktura projektu
- `projekt.py` – główny plik gry (logika + silnik)
- `README.txt` – instrukcja uruchomienia
- `assets/` – tworzony automatycznie katalog z podfolderami:
  - `images/` – grafiki
  - `sounds/` – dźwięki
  - `fonts/` – czcionki
  - `data/` – dane gry (JSON)

---

## Użyteczne funkcje w kodzie

| Funkcja                         | Opis                                                                 |
|----------------------------------|----------------------------------------------------------------------|
| `pygame.init()`                 | Inicjalizacja modułów Pygame                                         |
| `os.makedirs(..., exist_ok=True)` | Tworzenie katalogów bez błędu przy istnieniu                        |
| `pygame.display.set_mode()`     | Tworzy okno gry                                                      |
| `pygame.time.Clock()`           | Steruje liczbą klatek na sekundę (FPS)                               |
| `random.choice()`, `random.shuffle()` | Wybory i tasowanie elementów gry                                  |
| `pygame.event.get()`            | Obsługuje zdarzenia (np. klawiatura, mysz)                           |
| `pygame.draw.rect()`            | Rysowanie prostokątów (np. UI, gracz, przedmioty)                    |
| `pygame.font.Font()`            | Załaduj niestandardową czcionkę                                      |
| `pygame.mixer.Sound()`          | Odtwarzanie dźwięków                                                 |
| `time.time()`                   | Pomiar upływu czasu                                                  |
| `json.load()`, `json.dump()`    | Odczyt i zapis danych (przedmioty, wydarzenia)                       |

---

## Fazy gry

### 1. Faza Zbierania (60 sekund)
- Gracz porusza się po domu
- Zbiera przedmioty do schronu
- Odliczany jest czas 60 sekund

### 2. Faza Przetrwania
- Gra dzieli się na 30 dni
- Każdego dnia pojawiają się wydarzenia losowe
- Gracz decyduje, komu dać jedzenie, wodę, czy użyć medykamentów
- Zarządzane są: zdrowie, głód, pragnienie i psychika

---

## Wskazówki
- Jedzenie i woda to absolutna podstawa
- Medykamenty mogą uratować życie
- Broń i narzędzia pomagają w sytuacjach kryzysowych

---

## Uruchomienie gry

```bash
pip install pygame numpy
python projekt.py
