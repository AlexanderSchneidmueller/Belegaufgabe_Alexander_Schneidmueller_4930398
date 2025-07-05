# Zentrierung des Fensters auf die Mitte des Bildschirms beim Starten
import os
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Genutzte Bibliotheken
import pygame
import pgzrun
import random
import json

# Bildschirmeinstellungen
WIDTH = 1000
HEIGHT = 800
TITLE = "Guess what!?"

# Farbdefinitionen
BACKGROUND = (50, 50, 80)
TITLE_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 70, 120)
BUTTON_HOVER = (90, 90, 140)
TEXT_COLOR = (255, 255, 255)
CORRECT_COLOR = (0, 200, 0)
WRONG_COLOR = (200, 0, 0)
QUESTION_COLOR = (100, 100, 150)

# Spielzustände
MENU = 0
GAME = 1
SCORE = 2
HIGHSCORE = 3

# Globale Variablen
pending_score_screen = False
name_input_focused = False
cursor_visible = True
cursor_timer = 0
answer_feedback = [-1, -1, -1, -1]
buttons_locked = False

# Button-Klasse für interaktive Elemente
class Button:
    def __init__(self, x, y, width, height, text, action=None, color=None, hover_color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.is_hovered = False
        self.color = color or BUTTON_COLOR
        self.hover_color = hover_color or BUTTON_HOVER

    # Zeichnet den Button mit optionalem Feedback (richtig/falsch)
    def draw(self, feedback_state=-1):
        if feedback_state == 1:
            color = CORRECT_COLOR
        elif feedback_state == 0:
            color = WRONG_COLOR
        else:
            color = self.hover_color if self.is_hovered else self.color

        pygame.draw.rect(screen.surface, color, (self.x, self.y, self.width, self.height))
        screen.draw.text(self.text, center=(self.x + self.width // 2, self.y + self.height // 2), fontsize=24, color=TEXT_COLOR)

    # Prüft, ob Maus über Button ist
    def check_hover(self, pos):
        self.is_hovered = (
            self.x <= pos[0] <= self.x + self.width and
            self.y <= pos[1] <= self.y + self.height
        )
        return self.is_hovered

    # Behandelt Klick auf Button
    def handle_click(self, pos):
        if self.check_hover(pos) and self.action:
            self.action()

# Initialisiert alle Spielvariablen
def init():
    global current_state, score, current_question, feedback_timer, player_name
    global questions, answer_buttons, highscores
    global pending_score_screen, name_input_focused, cursor_visible, cursor_timer
    global answer_feedback, buttons_locked

    current_state = MENU
    score = 0
    current_question = 0
    feedback_timer = 0
    player_name = ""
    highscores = []

    # Reset aller Zustandsvariablen
    pending_score_screen = False
    name_input_focused = False
    cursor_visible = True
    cursor_timer = 0
    answer_feedback = [-1, -1, -1, -1]
    buttons_locked = False

    # Fragenkatalog
    questions = [
        {"question": "Was ist die Hauptstadt von Deutschland?", "answers": ["Berlin", "Paris", "London", "Madrid"], "correct": 0},
        {"question": "Wie viele Planeten hat unser Sonnensystem?", "answers": ["8", "9", "7", "10"], "correct": 0},
        {"question": "Welche Farbe hat eine reife Zitrone?", "answers": ["Gelb", "Grün", "Rot", "Blau"], "correct": 0},
        {"question": "Was ist 2+2?", "answers": ["4", "5", "3", "22"], "correct": 0},
        {"question": "Welches ist keine Primzahl?", "answers": ["1", "2", "3", "5"], "correct": 0},
        {"question": "Wie heißt der größte Ozean?", "answers": ["Pazifik", "Atlantik", "Indik", "Arktik"], "correct": 0},
        {"question": "Welches Tier ist das schnellste Landtier?", "answers": ["Gepard", "Löwe", "Gazelle", "Windhund"], "correct": 0},
        {"question": "Wie viele Tage hat ein Schaltjahr?", "answers": ["366", "365", "364", "367"], "correct": 0},
        {"question": "Welches ist keine Programmiersprache?", "answers": ["Kartoffel", "Python", "Java", "C++"], "correct": 0},
        {"question": "Was misst ein Thermometer?", "answers": ["Temperatur", "Druck", "Feuchtigkeit", "Lautstärke"], "correct": 0}
    ]

    # Antwort-Buttons erstellen
    answer_buttons = []
    for i in range(4):
        answer_buttons.append(Button(WIDTH // 2 - 300, HEIGHT // 2 + i * 70, 600, 60, ""))

    load_highscores()

# Initialisiert eine neue Spielrunde
def init_game():
    global score, current_question, feedback_timer, pending_score_screen
    global answer_feedback, buttons_locked

    score = 0
    current_question = 0
    feedback_timer = 0
    pending_score_screen = False
    random.shuffle(questions)
    answer_feedback = [-1, -1, -1, -1]
    buttons_locked = False

# Startet ein neues Spiel
def start_game():
    global current_state
    init_game()
    current_state = GAME

# Zeigt die Highscore-Liste an
def show_highscore():
    global current_state
    current_state = HIGHSCORE

# Beendet das Spiel
def quit_game():
    pygame.quit()
    quit()

# Zurück zum Hauptmenü
def back_to_menu():
    global current_state
    current_state = MENU

# Überprüft die angeklickte Antwort
def check_answer(answer_index):
    global score, feedback_timer, current_question, pending_score_screen
    global answer_feedback, buttons_locked

    if buttons_locked:
        return

    buttons_locked = True
    correct = questions[current_question]["correct"]

    # Markiert richtige und falsche Antwort
    for i in range(4):
        if i == correct:
            answer_feedback[i] = 1  # richtig
        elif i == answer_index:
            answer_feedback[i] = 0  # falsch

    if answer_index == correct:
        score += 1

    feedback_timer = 180  # 3 Sekunden Feedback bei 60 FPS

    if current_question + 1 >= len(questions):
        pending_score_screen = True # Zeigt den Score nach der letzten Frage an

# Speichert den Score in der Highscore-Liste
def save_score():
    global highscores, current_state, player_name

    if player_name.strip():
        highscores.append({"name": player_name.strip(), "score": score})
        highscores.sort(key=lambda x: x["score"], reverse=True)
        highscores = highscores[:10]
        save_highscores()
        current_state = HIGHSCORE

# Laden der Highscores aus der .json Datei
def load_highscores():
    global highscores
    if os.path.exists("highscores.json"):
        with open("highscores.json", "r") as f:
            highscores = json.load(f)

# Speichert die Highscores in die .json Datei
def save_highscores():
    with open("highscores.json", "w") as f:
        json.dump(highscores, f)

# Spiel initialisieren
init()

# Hauptmenü-Buttons
menu_buttons = [
    Button(WIDTH // 2 - 150, HEIGHT // 2 - 30, 300, 60, "Spiel starten", start_game),
    Button(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 60, "Highscores", show_highscore),
    Button(WIDTH // 2 - 150, HEIGHT // 2 + 130, 300, 60, "Beenden", quit_game)
]

# Highscore-Buttons
highscore_buttons = [
    Button(WIDTH // 2 - 150, HEIGHT // 2 + 180, 300, 60, "Neue Runde", start_game),
    Button(WIDTH // 2 - 150, HEIGHT // 2 + 250, 300, 60, "Hauptmenü", back_to_menu)
]

# Zeichnet den aktuellen Zustand
def draw():
    screen.fill(BACKGROUND)

    # Hauptmenü
    if current_state == MENU:
        screen.draw.text("Guess what?!", center=(WIDTH // 2, HEIGHT // 4), fontsize=60, color=TITLE_COLOR)
        for button in menu_buttons:
            button.draw()

    # Spielansicht
    elif current_state == GAME:
        if current_question < len(questions):
            # Frage anzeigen
            pygame.draw.rect(screen.surface, QUESTION_COLOR, (50, 100, WIDTH - 100, 100))
            screen.draw.text(questions[current_question]["question"], center=(WIDTH // 2, 150), fontsize=30, color=TEXT_COLOR, scolor="black")
            # Antwortmöglichkeiten Anzeigen
            for i, button in enumerate(answer_buttons):
                button.text = questions[current_question]["answers"][i]
                button.draw(answer_feedback[i])
            # Punkte und Fortschritt anzeigen
            screen.draw.text(f"Punkte: {score} | Frage: {current_question + 1}/{len(questions)}", topleft=(20, 20), fontsize=24, color=TEXT_COLOR)

    # Ergebnisanzeige
    elif current_state == SCORE:
        global name_input_focused
        name_input_focused = True

        screen.draw.text("Spiel beendet!", center=(WIDTH // 2, HEIGHT // 4), fontsize=60, color=TITLE_COLOR)
        screen.draw.text(f"Dein Score: {score}/{len(questions)}", center=(WIDTH // 2, HEIGHT // 3), fontsize=40, color=TEXT_COLOR)
        screen.draw.text("Gib deinen Namen ein:", center=(WIDTH // 2, HEIGHT // 2), fontsize=30, color=TEXT_COLOR)

        # Name-Eingabefeld
        pygame.draw.rect(screen.surface, BUTTON_COLOR, (WIDTH // 2 - 150, HEIGHT // 2 + 30, 300, 50))
        name_display = player_name + ("|" if name_input_focused and cursor_visible else "")
        # Blinkender Cursor
        screen.draw.text(name_display, center=(WIDTH // 2, HEIGHT // 2 + 55), fontsize=30, color=TEXT_COLOR)

        # Speichern-Button
        Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "Speichern", save_score).draw()

        # Warnung wenn Name leer ist
        if not player_name.strip():
            screen.draw.text("Bitte gib einen Namen ein!", center=(WIDTH // 2, HEIGHT // 2 + 170), fontsize=20, color=WRONG_COLOR)

    # Highscore-Liste anzeigen
    elif current_state == HIGHSCORE:
        screen.draw.text("Highscores", center=(WIDTH // 2, 50), fontsize=60, color=TITLE_COLOR)
        for i, entry in enumerate(highscores[:10]):
            screen.draw.text(f"{i + 1}. {entry['name']}: {entry['score']}/{len(questions)}", center=(WIDTH // 2, 120 + i * 40), fontsize=30, color=TEXT_COLOR)
        for button in highscore_buttons:
            button.draw()

# Behandelt Tastatureingaben
def on_key_down(key):
    global player_name

    if current_state == SCORE and name_input_focused:
        if key == pygame.K_BACKSPACE:
            player_name = player_name[:-1]
        elif key == pygame.K_RETURN:
            save_score()
        elif len(player_name) < 15:
            key_char = key.name
            if len(key_char) == 1:
                player_name += key_char

# Behandelt Mausbewegungen für Hover-Effekte
def on_mouse_move(pos):
    buttons = []
    if current_state == MENU:
        buttons = menu_buttons
    elif current_state == GAME:
        buttons = answer_buttons
    elif current_state == HIGHSCORE:
        buttons = highscore_buttons

    for button in buttons:
        button.check_hover(pos)

# Behandelt Mausklicks
def on_mouse_down(pos):
    global name_input_focused

    if current_state == MENU:
        for button in menu_buttons:
            button.handle_click(pos)
    elif current_state == GAME:
        if not buttons_locked:
            for i, button in enumerate(answer_buttons):
                if button.check_hover(pos):
                    check_answer(i)
    # Name-Eingabefeld auswählen
    elif current_state == SCORE:
        if WIDTH // 2 - 150 <= pos[0] <= WIDTH // 2 + 150 and HEIGHT // 2 + 30 <= pos[1] <= HEIGHT // 2 + 80:
            name_input_focused = True
        else:
            name_input_focused = False

        # Speichern-Button
        if WIDTH // 2 - 100 <= pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 100 <= pos[1] <= HEIGHT // 2 + 150:
            save_score()
    elif current_state == HIGHSCORE:
        for button in highscore_buttons:
            button.handle_click(pos)

# Aktualisiert den Spielzustand (wird regelmäßig aufgerufen)
def update():
    global feedback_timer, current_state, pending_score_screen
    global cursor_timer, cursor_visible
    global answer_feedback, buttons_locked, current_question

    # Feedback-Timer
    if feedback_timer > 0:
        feedback_timer -= 1
    elif pending_score_screen:      # Nach letzter Frage
        current_state = SCORE
        pending_score_screen = False
    elif buttons_locked:            # Feedback vorbei
        buttons_locked = False
        answer_feedback = [-1, -1, -1, -1]      # Resettet Feedback
        current_question += 1       # Nächste Frage

    # Cursor-Blinken beim Namen Eingeben
    cursor_timer += 1
    if cursor_timer >= 30:
        cursor_visible = not cursor_visible
        cursor_timer = 0

# Startet Spiel
pgzrun.go()
