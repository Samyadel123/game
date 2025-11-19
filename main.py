import pygame
import random
import time

# --- Game Configuration ---
# The list of items to match: (word, "picture" representation)
# In Pygame, we use text representations for both words and pictures (emojis/short names).
GAME_ITEMS = {
    "Apple": "🍎 (Fruit)",
    "Car": "🚗 (Vehicle)",
    "Dog": "🐕 (Pet)",
    "Sun": "☀️ (Sky)",
    "Tree": "🌳 (Plant)",
    "Book": "📚 (Reading)",
    "Pizza": "🍕 (Food)",
    "Cat": "🐈 (Feline)",
}

# --- Pygame Initialization ---
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 50, 200)
GREEN = (34, 197, 94)
RED = (255, 99, 71)

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Picture Word Match")

# Fonts
FONT_SIZE = 24
CARD_FONT = pygame.font.Font(None, FONT_SIZE)
TITLE_FONT = pygame.font.Font(None, 48)

# Card dimensions
CARD_WIDTH = 150
CARD_HEIGHT = 80
CARD_MARGIN = 15
GRID_COLS = 4  # 8 pairs * 2 cards = 16 cards total (4x4 grid)
GRID_ROWS = 4

# --- Card Class Definition ---
class Card:
    """Represents a single card in the game."""
    def __init__(self, rect, value, match_key, card_type):
        self.rect = rect
        self.value = value
        self.match_key = match_key  # The word used for matching
        self.type = card_type       # 'word' or 'picture'
        self.is_flipped = False
        self.is_matched = False
        self.color = GRAY
        self.flipped_color = BLUE
        self.matched_color = GREEN

    def draw(self, surface):
        """Draws the card on the screen."""
        if self.is_matched:
            # Draw matched cards with green border
            pygame.draw.rect(surface, self.matched_color, self.rect, 0, 8)
            pygame.draw.rect(surface, GREEN, self.rect, 5, 8)
            # Display value on matched cards
            text_surface = CARD_FONT.render(self.value, True, BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
        elif self.is_flipped:
            # Draw flipped cards (showing value)
            pygame.draw.rect(surface, self.flipped_color, self.rect, 0, 8)
            text_surface = CARD_FONT.render(self.value, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
        else:
            # Draw unflipped cards (showing back)
            pygame.draw.rect(surface, self.color, self.rect, 0, 8)
            # Draw a question mark or card type on the back
            back_text = CARD_FONT.render("?", True, BLACK)
            text_rect = back_text.get_rect(center=self.rect.center)
            surface.blit(back_text, text_rect)

    def handle_event(self, event):
        """Handles mouse clicks on the card."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and not self.is_flipped and not self.is_matched:
                self.is_flipped = True
                return True # Indicate that the card was successfully flipped
        return False

# --- Game Functions ---

def create_card_set():
    """Generates and shuffles all card objects."""
    cards = []
    
    # Calculate starting position for centering the grid
    grid_width = GRID_COLS * CARD_WIDTH + (GRID_COLS - 1) * CARD_MARGIN
    grid_height = GRID_ROWS * CARD_HEIGHT + (GRID_ROWS - 1) * CARD_MARGIN
    start_x = (SCREEN_WIDTH - grid_width) // 2
    start_y = (SCREEN_HEIGHT - grid_height) // 2

    # Create card objects
    temp_card_list = []
    for word, picture in GAME_ITEMS.items():
        # Word Card
        temp_card_list.append({
            'value': word,
            'match_key': word,
            'type': 'word'
        })
        # Picture Card
        temp_card_list.append({
            'value': picture,
            'match_key': word,
            'type': 'picture'
        })
        
    random.shuffle(temp_card_list)

    # Assign positions and create Card instances
    for i, data in enumerate(temp_card_list):
        row = i // GRID_COLS
        col = i % GRID_COLS
        
        x = start_x + col * (CARD_WIDTH + CARD_MARGIN)
        y = start_y + row * (CARD_HEIGHT + CARD_MARGIN)
        
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        cards.append(Card(rect, data['value'], data['match_key'], data['type']))
        
    return cards

def draw_info(surface, matches, attempts):
    """Draws the score and attempts."""
    total_pairs = len(GAME_ITEMS)
    score_text = CARD_FONT.render(f"Matches: {matches}/{total_pairs}", True, BLACK)
    attempts_text = CARD_FONT.render(f"Attempts: {attempts}", True, BLACK)
    
    # Draw title
    title_surface = TITLE_FONT.render("Picture Word Match Game", True, BLACK)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    surface.blit(title_surface, title_rect)
    
    # Draw stats
    surface.blit(score_text, (20, 100))
    surface.blit(attempts_text, (SCREEN_WIDTH - attempts_text.get_width() - 20, 100))

# --- Main Game Loop ---
def main():
    running = True
    clock = pygame.time.Clock()

    all_cards = create_card_set()
    flipped_cards = []
    matches_found = 0
    attempts = 0
    game_locked = False
    lock_timer = 0

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Allow 'Q' key to quit the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
            
            if not game_locked:
                for card in all_cards:
                    if card.handle_event(event):
                        # A card was flipped
                        flipped_cards.append(card)
                        
                        if len(flipped_cards) == 2:
                            attempts += 1
                            game_locked = True
                            lock_timer = pygame.time.get_ticks()

        # Check for match when two cards are flipped
        if game_locked and (pygame.time.get_ticks() - lock_timer > 1200): # Check after 1.2 seconds
            card1, card2 = flipped_cards[0], flipped_cards[1]
            
            # Check conditions for a valid match: same key AND different types (word vs picture)
            if card1.match_key == card2.match_key and card1.type != card2.type:
                card1.is_matched = True
                card2.is_matched = True
                matches_found += 1
                # Make matched cards bright green immediately
                card1.flipped_color = GREEN 
                card2.flipped_color = GREEN
            else:
                # If no match, flip them back
                card1.is_flipped = False
                card2.is_flipped = False

            # Reset state for the next turn
            flipped_cards = []
            game_locked = False
        
        # --- Drawing ---
        SCREEN.fill(WHITE)
        
        # Draw all cards
        for card in all_cards:
            card.draw(SCREEN)

        # Draw info
        draw_info(SCREEN, matches_found, attempts)

        # Check for win condition
        if matches_found == len(GAME_ITEMS):
            win_text = TITLE_FONT.render("🎉 YOU WON!", True, GREEN)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            SCREEN.blit(win_text, win_rect)

            # Add instructions on how to close
            close_text = CARD_FONT.render("Press 'Q' or close the window (X) to exit.", True, BLACK)
            close_rect = close_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            SCREEN.blit(close_text, close_rect)
        
        # Update the full display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()