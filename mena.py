import tkinter as tk
from PIL import Image, ImageTk

# ---------------- STATES ------------------
class GameState:
    MENU = "menu"
    LEVEL1 = "level1"

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
button_img = ImageTk.PhotoImage(Image.open("button.png").resize((400, 150)))
# -------------------------------------------

# ---------------- WIDGETS ------------------
canvas = tk.Canvas(root, width=900, height=1000)
canvas.pack()

def start_game():
    print("Button Pressed!")
    state_manager.change_state(GameState.LEVEL1)

start_button = tk.Button(root, image=button_img, command=start_game, borderwidth=0)
# -------------------------------------------

# ------------ SCREEN RENDERING -------------
def update_screen():
    canvas.delete("all")

    if state_manager.state == GameState.MENU:
        canvas.create_image(0, 0, anchor="nw", image=menu_bg_img)
        canvas.create_window(450, 600, window=start_button)

    elif state_manager.state == GameState.LEVEL1:
        canvas.create_image(0, 0, anchor="nw", image=level1_bg_img)

        # 🔥 Level 1 logic goes here
        # Example:
        # draw player, run timers, etc.
        # For animations you'd need canvas movement functions

# -------------------------------------------

update_screen()
root.mainloop()
