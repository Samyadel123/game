import tkinter as tk
from PIL import Image, ImageTk
import random
import winsound

# ---------------- STATES ------------------
class GameState:
    MENU = "menu"
    LEVEL1 = "level1"
    LEVEL1_PLAY = "level1_play"
    LEVEL1_WIN = "level1_win"   # Win screen


class GameStateManager:
    def __init__(self, root):
        self.state = GameState.MENU
        self.root = root

    def change_state(self, new_state):
        self.state = new_state
        update_screen()


# ---------------- MAIN WINDOW ------------------
root = tk.Tk()
root.title("لعبه الذاكره")
root.geometry("900x1000")

state_manager = GameStateManager(root)

# ---------------- IMAGES ------------------
menu_bg_img = ImageTk.PhotoImage(Image.open("background.jpeg").resize((900, 1000)))
level1_bg_img = ImageTk.PhotoImage(Image.open("background2.jpeg").resize((900, 1000)))
level1_play_bg_img = ImageTk.PhotoImage(Image.open("leve1.jpeg").resize((900, 1000)))

button_img = ImageTk.PhotoImage(
    Image.open("Gemini_Generated_Image_3xbhm83xbhm83xbh (1).png").resize((400, 150))
)

card_back = ImageTk.PhotoImage(Image.open("card.jpeg").resize((150, 150)))

cup_img = ImageTk.PhotoImage(Image.open("cup.jpeg").resize((300, 300)))

# ---------------- GAME VARIABLES ------------------
cards = []
buttons = []
first_pick = None
second_pick = None
matched_pairs = 0
attempts = 0
attempt_text = None
card_images = []  # store card images globally to prevent garbage collection

# ---------------- WIDGETS ------------------
canvas = tk.Canvas(root, width=900, height=1000)
canvas.pack()

def start_game():
    state_manager.change_state(GameState.LEVEL1)

def begin_level1():
    state_manager.change_state(GameState.LEVEL1_PLAY)

start_button = tk.Button(root, image=button_img, command=start_game, borderwidth=0)
level1_start_button = tk.Button(root, text="ابدأ", command=begin_level1,
                                font=("Arial", 24))

# ---------------- MEMORY GAME LOGIC ------------------
def setup_memory_game():
    global cards, buttons, first_pick, second_pick, matched_pairs, attempts, attempt_text, card_images

    first_pick = None
    second_pick = None
    matched_pairs = 0
    attempts = 0
    buttons.clear()
    card_images.clear()

    # Load images
    img_earth = ImageTk.PhotoImage(Image.open("earth.jpeg").resize((150,150)))
    img_blue  = ImageTk.PhotoImage(Image.open("bleue.jpeg").resize((150,150)))
    img_red   = ImageTk.PhotoImage(Image.open("red.jpeg").resize((150,150)))
    img_sun   = ImageTk.PhotoImage(Image.open("sun.jpeg").resize((150,150)))

    card_images.extend([img_earth, img_blue, img_red, img_sun])

    # Prepare shuffled card IDs
    card_ids = list(range(4)) * 4
    random.shuffle(card_ids)
    cards[:] = card_ids  # keep global reference

    # Display attempts text
    global attempt_text
    attempt_text = canvas.create_text(
        450, 150,
        text="Attempts: 0",
        fill="white",
        font=("Arial", 28)
    )

    # Create card buttons
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

def flip_card(index):
    global first_pick, second_pick

    btn = buttons[index]
    if btn["state"] == "disabled":
        return

    btn.config(image=card_images[cards[index]], state="disabled")

    if first_pick is None:
        first_pick = index
    else:
        second_pick = index
        root.after(700, check_match)

def check_match():
    global first_pick, second_pick, matched_pairs, attempts

    i, j = first_pick, second_pick

    if cards[i] == cards[j]:
        matched_pairs += 1

        # WIN CONDITION
        if matched_pairs == 8:
            state_manager.change_state(GameState.LEVEL1_WIN)
            try:
                winsound.PlaySound("claping.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            except:
                print("Could not play claping.wav")
    else:
        attempts += 1
        canvas.itemconfig(attempt_text, text=f"Attempts: {attempts}")
        buttons[i].config(image=card_back, state="normal")
        buttons[j].config(image=card_back, state="normal")

    first_pick = None
    second_pick = None

# ---------------- SCREEN RENDERING ------------------
def update_screen():
    canvas.delete("all")

    if state_manager.state == GameState.MENU:
        canvas.create_image(0, 0, anchor="nw", image=menu_bg_img)
        canvas.create_window(450, 600, window=start_button)

    elif state_manager.state == GameState.LEVEL1:
        canvas.create_image(0, 0, anchor="nw", image=level1_bg_img)
        canvas.create_window(450, 800, window=level1_start_button)

    elif state_manager.state == GameState.LEVEL1_PLAY:
        canvas.create_image(0, 0, anchor="nw", image=level1_play_bg_img)
        setup_memory_game()  # create cards

    elif state_manager.state == GameState.LEVEL1_WIN:
        canvas.create_image(0, 0, anchor="nw", image=level1_play_bg_img)
        canvas.create_image(450, 500, image=cup_img)
        canvas.create_text(
            450, 200,
            text="🎉 احسنت! لقد أكملت اللعبة 🎉",
            fill="yellow",
            font=("Arial", 36, "bold")
        )

# ---------------- RUN ------------------
update_screen()
root.mainloop()
