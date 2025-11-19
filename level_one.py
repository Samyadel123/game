import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((900, 1000))
pygame.display.set_caption("Button!")
main_font = pygame.font.SysFont("cambria", 50)

# ---------------- STATES ------------------
class GameState:
    MENU = "menu"
    LEVEL1 = "level1"

class GameStateManager:
    def __init__(self):
        self.state = GameState.MENU

    def change_state(self, new_state):
        self.state = new_state

state_manager = GameStateManager()
# ------------------------------------------

# ------------ LOAD RESOURCES ---------------
background_menu = pygame.image.load("background.jpeg")
background_level1 = pygame.image.load("background2.jpeg")
# -------------------------------------------

class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(x_pos, y_pos))

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if self.rect.collidepoint(position):
            print("Button Press!")
            state_manager.change_state(GameState.LEVEL1)

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = main_font.render(self.text_input, True, "green")
        else:
            self.text = main_font.render(self.text_input, True, "white")


# ---------------- BUTTON -------------------
button_surface = pygame.image.load("button.png")
button_surface = pygame.transform.scale(button_surface, (400, 150))
button = Button(button_surface, 450, 600, "Start Game")
# -------------------------------------------

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state_manager.state == GameState.MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                button.checkForInput(pygame.mouse.get_pos())

    # ------------- RENDER BY STATE ----------------
    if state_manager.state == GameState.MENU:
        screen.blit(background_menu, (0, 0))
        button.changeColor(pygame.mouse.get_pos())
        button.update()

    elif state_manager.state == GameState.LEVEL1:
        screen.blit(background_level1, (0, 0))

        # 🔥🔥🔥 LEVEL 1 LOGIC GOES HERE 🔥🔥🔥
        # Example:
        # player.update()
        # enemies.update()
        # draw_score()
        # print("level 1 running")

    pygame.display.update()
