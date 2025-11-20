import tkinter as tk
from PIL import Image, ImageTk

# ---------------- STATES ------------------
class GameState:
    MENU = "menu"
    LEVEL1 = "level1"
    LEVEL1_PLAY = "level1_play"   # ⭐ NEW STATE

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
level1_play_bg_img = ImageTk.PhotoImage(Image.open("leve1.jpeg").resize((900, 1000)))   # ⭐ NEW BACKGROUND

button_img = ImageTk.PhotoImage(Image.open("Gemini_Generated_Image_3xbhm83xbhm83xbh (1).png").resize((400, 150)))

# -------------------------------------------

# ---------------- WIDGETS ------------------
canvas = tk.Canvas(root, width=900, height=1000)
canvas.pack()

def start_game():
    state_manager.change_state(GameState.LEVEL1)

def begin_level1():
    state_manager.change_state(GameState.LEVEL1_PLAY)

start_button = tk.Button(root, image=button_img, command=start_game, borderwidth=0)

# ⭐ NEW LEVEL 1 START BUTTON
level1_start_button = tk.Button(root, text="Start Level 1", font=("Arial", 24),
                                command=begin_level1)

# -------------------------------------------

# ------------ SCREEN RENDERING -------------
def update_screen():
    canvas.delete("all")

    # ------ MENU SCREEN ------
    if state_manager.state == GameState.MENU:
        canvas.create_image(0, 0, anchor="nw", image=menu_bg_img)
        canvas.create_window(450, 600, window=start_button)

    # ------ LEVEL 1 SCREEN ------
    elif state_manager.state == GameState.LEVEL1:
        canvas.create_image(0, 0, anchor="nw", image=level1_bg_img)

        # ⭐ Place Level 1 start button
        canvas.create_window(450, 800, window=level1_start_button)

    # ------ LEVEL 1 PLAY SCREEN ------
    elif state_manager.state == GameState.LEVEL1_PLAY:
        canvas.create_image(0, 0, anchor="nw", image=level1_play_bg_img)

        # 🔥 Level 1 gameplay code goes here
        canvas.create_text(450, 100, text="LEVEL 1 STARTED!", fill="white", font=("Arial", 40))

# -------------------------------------------

update_screen()
root.mainloop()
