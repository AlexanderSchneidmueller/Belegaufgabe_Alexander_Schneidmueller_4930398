# Deklaration der Importe
import pygame
import pgzrun

# Deklaration der Variablen
WIDTH = 800
HEIGHT = 600
TITLE = "Guess what!?"

# Deklaration der Farben einzelner Elemente
BACKGROUND = (50, 50, 80)
TITLE_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 70, 120)
BUTTON_HOVER = (90, 90, 140)
TEXT_COLOR = (255, 255, 255)

# Button-Klasse
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self):
        color = BUTTON_HOVER if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(screen.surface, color, (self.x, self.y, self.width, self.height))
        screen.draw.text(
            self.text,
            center=(self.x + self.width // 2, self.y + self.height // 2),
            fontsize=30,
            color=TEXT_COLOR
        )

    def check_hover(self, pos):
        self.is_hovered = (
            self.x <= pos[0] <= self.x + self.width and
            self.y <= pos[1] <= self.y + self.height
        )
        return self.is_hovered

    def handle_click(self, pos):
        if self.check_hover(pos) and self.action:
            self.action()

# Menü-Aktionen
def start_game():
    print("Spiel starten!")

def show_highscore():
    print("Highscores")

def quit_game():
    print("Beenden")
    pygame.quit()
    quit()

# Buttons erstellen
buttons = [
    Button(WIDTH // 2 - 150, HEIGHT // 2 - 30, 300, 60, "Spiel starten", start_game),
    Button(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 60, "Highscores", show_highscore),
    Button(WIDTH // 2 - 150, HEIGHT // 2 + 130, 300, 60, "Beenden", quit_game)
]

def draw():
    screen.fill(BACKGROUND)

    # Titel
    screen.draw.text(
        "Guess what?!",
        center=(WIDTH // 2, HEIGHT // 4),
        fontsize=60,
        color=TITLE_COLOR
    )

    # Buttons
    for button in buttons:
        button.draw()

def on_mouse_move(pos):
    for button in buttons:
        button.check_hover(pos)

def on_mouse_down(pos):
    for button in buttons:
        button.handle_click(pos)

# Spiel starten
pgzrun.go()