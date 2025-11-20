import tkinter as tk
from PIL import Image, ImageTk
import random

# ---------------- STATES ------------------
class GameState:
    MENU = "menu"
    LEVEL1 = "level1"
    LEVEL1_PLAY = "level1_play"

class GameStateManager:
    def __init__(self, root):
        self.state = GameState.MENU
        self.root = root

    def change_state(self, new_state):
        self.state = new_state
        update_screen()


# Main Window
root = tk.Tk()
root.title("Button Game")
root.geometry("900x1000")

state_manager = GameStateManager(root)

# ---------------- IMAGES ------------------
menu_bg_img = ImageTk.PhotoImage(Image.open("background.jpeg").resize((900, 1000)))
level1_bg_img = ImageTk.PhotoImage(Image.open("background2.jpeg").resize((900, 1000)))
level1_play_bg_img = ImageTk.PhotoImage(Image.open("leve1.jpeg").resize((900, 1000)))

button_img = ImageTk.PhotoImage(
    Image.open("Gemini_Generated_Image_3xbhm83xbhm83xbh (1).png").resize((400, 150))
)

# Card back
card_back = ImageTk.PhotoImage(Image.open("background.jpeg").resize((150, 150)))

# Memory game variables
cards = []
buttons = []
first_pick = None
second_pick = None
matched_pairs = 0
attempts = 0


# ---------------- WIDGETS ------------------
canvas = tk.Canvas(root, width=900, height=1000)
canvas.pack()

def start_game():
    state_manager.change_state(GameState.LEVEL1)

def begin_level1():
    state_manager.change_state(GameState.LEVEL1_PLAY)

start_button = tk.Button(root, image=button_img, command=start_game, borderwidth=0)
level1_start_button = tk.Button(root, text="Start Level 1", command=begin_level1,
                                font=("Arial", 24))


# -----------------------------------------------------
#               MEMORY GAME LOGIC
# -----------------------------------------------------

def setup_memory_game():
    global cards, buttons, first_pick, second_pick, matched_pairs, attempts, attempt_text, card_images

    first_pick = None
    second_pick = None
    matched_pairs = 0
    attempts = 0
    buttons.clear()

    # Load images one time
    img_earth = ImageTk.PhotoImage(Image.open("earth.jpeg").resize((150,150)))
    img_blue  = ImageTk.PhotoImage(Image.open("bleue.jpeg").resize((150,150)))
    img_red   = ImageTk.PhotoImage(Image.open("red.jpeg").resize((150,150)))
    img_sun   = ImageTk.PhotoImage(Image.open("sun.jpeg").resize((150,150)))

    # Store image objects in index order
    card_images = [img_earth, img_blue, img_red, img_sun]

    # Make a list of IDs (0–3 repeated 4 times → 16 cards)
    card_ids = list(range(4)) * 4  # 4 unique images × 4 copies = 16 cards

    random.shuffle(card_ids)

    cards = card_ids  # store IDs instead of PhotoImage

    # Draw attempt counter
    attempt_text = canvas.create_text(
        450, 150,
        text="Attempts: 0",
        fill="white",
        font=("Arial", 28)
    )



def flip_card(index):
    global first_pick, second_pick

    btn = buttons[index]

    if btn["state"] == "disabled":
        return

    # Show the correct image
    btn.config(image=card_images[cards[index]], state="disabled")

    if first_pick is None:
        first_pick = index
    else:
        second_pick = index
        root.after(700, check_match)


def check_match():
    global first_pick, second_pick, matched_pairs, attempts

    i, j = first_pick, second_pick

    # MATCH: same ID
    if cards[i] == cards[j]:
        matched_pairs += 1

        if matched_pairs == 8:  # all 16 cards matched
            canvas.create_text(
                450, 70,
                text="🎉 YOU DID IT! 🎉",
                fill="yellow",
                font=("Arial", 42)
            )

    else:
        attempts += 1
        canvas.itemconfig(attempt_text, text=f"Attempts: {attempts}")

        buttons[i].config(image=card_back, state="normal")
        buttons[j].config(image=card_back, state="normal")

    first_pick = None
    second_pick = None


# -----------------------------------------------------
#                 SCREEN RENDERING
# -----------------------------------------------------
def update_screen():
    canvas.delete("all")

    # ------ MENU ------
    if state_manager.state == GameState.MENU:
        canvas.create_image(0, 0, anchor="nw", image=menu_bg_img)
        canvas.create_window(450, 600, window=start_button)

    # ------ LEVEL 1 ------
    elif state_manager.state == GameState.LEVEL1:
        canvas.create_image(0, 0, anchor="nw", image=level1_bg_img)
        canvas.create_window(450, 800, window=level1_start_button)

    # ------ LEVEL 1 PLAY (MEMORY GAME) ------
    elif state_manager.state == GameState.LEVEL1_PLAY:
        canvas.create_image(0, 0, anchor="nw", image=level1_play_bg_img)

        setup_memory_game()

        x_start = 150
        y_start = 200
        index = 0

        for row in range(4):
            for col in range(4):
                btn = tk.Button(root, image=card_back,
                                command=lambda i=index: flip_card(i),
                                borderwidth=0)
                buttons.append(btn)
                canvas.create_window(
                    x_start + col * 170,
                    y_start + row * 170,
                    window=btn
                )
                index += 1


# -----------------------------------------------------

update_screen()
root.mainloop()
