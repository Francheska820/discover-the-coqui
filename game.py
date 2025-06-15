

"""This is a simple click-and-score game for two players. It's inspired by the coquí, a famous frog from Puerto Rico.
How to Play:
    Each player has limited time to find and click the coquí that appears randomly on the screen. Every successful click earns a point.
Game Flow:
    1. The game starts with a title screen. Click to begin.
    2. Player 1 gets 30 seconds to find coquís.
    3. When Player 1's time is up, it's Player 2's turn.
    4. Player 2 also gets 30 seconds to find coquís.
    5. After both turns, the game shows who won (or if it's a tie) based on scores.
    6. Click on the "Game Over" screen to play again.
Visuals:
    - A background image showing Puerto Rico scenery.
    - A coquí image to click on.
    - Trees and flowers are just for looks (they don't affect gameplay).
Have fun discovering the coquí!"""

import pygame
import random
import time
import sys 

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Discover the Coquí") 

# Colors (RGB)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Fonts
font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

# Load images
background_image = pygame.image.load('puertorico_background.jpg')
coqui_image = pygame.image.load('coqui.png')
tree_image = pygame.image.load('tree.png')
flower_image = pygame.image.load('flower.png')

# Load background music
pygame.mixer.music.load('tropical_forest_puertorico.mp3')
pygame.mixer.music.set_volume(0.5)  # Set the volume to 50%

# Scale background to game dimensions
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Scale object images
COQUI_SIZE = 80
OBSTACLE_SIZE = 80
coqui_image = pygame.transform.scale(coqui_image, (COQUI_SIZE, COQUI_SIZE))
tree_image = pygame.transform.scale(tree_image, (OBSTACLE_SIZE, OBSTACLE_SIZE))
flower_image = pygame.transform.scale(flower_image, (OBSTACLE_SIZE, int(OBSTACLE_SIZE * 0.6))) # Flower might be wider than tall

# Function to display score for players
def display_score(player_score, player_number, position_y):
    text_color = WHITE
    if player_number == 1:
        text_color = BLUE # Player 1 score in blue
    else:
        text_color = RED # Player 2 score in red

    text = font_medium.render(f"Player {player_number} Score: {player_score}", True, text_color)
    screen.blit(text, (10, position_y))

# Function to display time remaining
def display_time(time_left):
    time_text = font_medium.render(f"Time: {max(0, time_left)}", True, WHITE) # Ensure time doesn't go negative
    screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

# Function to display messages on screen ("Time's up!", "Player Wins!")
def display_message(message, color, font_size=font_large):
    text = font_size.render(message, True, color)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    time.sleep(1.5) # Keep message on screen for 1.5 seconds

# Main game function
def game():
    time_limit = 30 # Time limit for each player (in seconds)
    clock = pygame.time.Clock()

    running = True
    game_state = "START_SCREEN" # States: START_SCREEN, PLAYER1_TURN, PLAYER2_TURN, GAME_OVER

    score_player1 = 0
    score_player2 = 0

    # Random positions for trees and flowers (obstacles)
    obstacles = []
    for _ in range(5):
        obj_type = random.choice(["tree", "flower"])
        obj_width = OBSTACLE_SIZE
        obj_height = OBSTACLE_SIZE if obj_type == "tree" else int(OBSTACLE_SIZE * 0.6)
        
        # Ensure obstacles are within screen bounds
        x = random.randint(50, WIDTH - obj_width - 50)
        y = random.randint(50, HEIGHT - obj_height - 50)
        obstacles.append({"type": obj_type, "rect": pygame.Rect(x, y, obj_width, obj_height)})

    # Coquí position (initialized, will be randomized at start of each turn)
    coqui_rect = pygame.Rect(0, 0, COQUI_SIZE, COQUI_SIZE)

    def set_random_coqui_position():
        """Sets a new random position for the coquí."""
        coqui_rect.x = random.randint(COQUI_SIZE, WIDTH - COQUI_SIZE)
        coqui_rect.y = random.randint(COQUI_SIZE, HEIGHT - COQUI_SIZE)

    # Initial setup for game start
    set_random_coqui_position() # Set initial coquí position

    # Play background music when the game starts.
    if pygame.mixer.music.get_busy() == 0: # Only play if not already playing (e.g., from a previous game loop run)
        pygame.mixer.music.play(-1) # -1 makes it loop indefinitely

    while running:
        screen.blit(background_image, (0, 0)) # Draw background first

        if game_state == "START_SCREEN":
            display_message("Click to Start", WHITE, font_large)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "PLAYER1_TURN"
                    start_time = time.time() # Start timer for Player 1
                    score_player1 = 0
                    score_player2 = 0 # Reset scores on new game start
                    set_random_coqui_position() # New coquí for start of P1 turn

        elif game_state == "PLAYER1_TURN":
            current_time = time.time()
            elapsed_time = current_time - start_time
            time_left = int(time_limit - elapsed_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the click was on the coquí
                    if coqui_rect.collidepoint(event.pos):
                        score_player1 += 1
                        set_random_coqui_position() # Move coquí

            # Draw obstacles
            for obj in obstacles:
                if obj["type"] == "tree":
                    screen.blit(tree_image, obj["rect"])
                else:
                    screen.blit(flower_image, obj["rect"])

            # Draw the coquí
            screen.blit(coqui_image, coqui_rect)

            # Display score and time
            display_score(score_player1, 1, 10) # Player 1 score at top left
            display_score(score_player2, 2, 60) # Player 2 score slightly below
            display_time(time_left)

            if time_left <= 0:
                display_message("Time's up! Player 1's Turn Over.", WHITE, font_medium)
                game_state = "PLAYER2_TURN"
                start_time = time.time() # Reset timer for Player 2
                set_random_coqui_position() # New coquí for start of P2 turn

        elif game_state == "PLAYER2_TURN":
            current_time = time.time()
            elapsed_time = current_time - start_time
            time_left = int(time_limit - elapsed_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the click was on the coquí
                    if coqui_rect.collidepoint(event.pos):
                        score_player2 += 1
                        set_random_coqui_position() # Move coquí

            # Draw obstacles
            for obj in obstacles:
                if obj["type"] == "tree":
                    screen.blit(tree_image, obj["rect"])
                else:
                    screen.blit(flower_image, obj["rect"])

            # Draw the coquí
            screen.blit(coqui_image, coqui_rect)

            # Display score and time
            display_score(score_player1, 1, 10)
            display_score(score_player2, 2, 60)
            display_time(time_left)

            if time_left <= 0:
                display_message("Time's up! Player 2's Turn Over.", WHITE, font_medium)
                game_state = "GAME_OVER"

        elif game_state == "GAME_OVER":
            # Determine winner
            if score_player1 > score_player2:
                final_message = f"Player 1 Wins with {score_player1} points!"
                message_color = BLUE
            elif score_player2 > score_player1:
                final_message = f"Player 2 Wins with {score_player2} points!"
                message_color = RED
            else:
                final_message = f"It's a Tie! Both {score_player1} points."
                message_color = BLACK

            display_message(final_message, message_color, font_large)
            display_message("Click to Play Again", WHITE, font_medium) # Prompt to restart
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "START_SCREEN" # Restart game from start screen

        pygame.display.flip() # Update the full display surface
        clock.tick(60) # Limit FPS to 60

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == '__main__':
    game()
