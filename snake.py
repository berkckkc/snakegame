import pygame
import sys
import random

# Initialize game
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
orange = (255, 128, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
gray = (200, 200, 200)
dark_gray = (100, 100, 100)

# Cell size
cell_size = 20

# Initial game state
def init_game():
    return {
        "snake": [(100, 100), (80, 100), (60, 100)],
        "direction": "RIGHT",
        "color": orange,
        "food": spawn_food(),
        "score": 0,
        "game_over": False
    }

# Spawn food at a random location
def spawn_food():
    x = random.randint(1, (screen_width - cell_size*2) // cell_size) * cell_size
    y = random.randint(1, (screen_height - cell_size*2) // cell_size) * cell_size
    return (x, y)

# Change snake color
def change_color(state):
    state["color"] = white if state["color"] == orange else orange

# Move snake in the current direction
def move_snake(state):
    x, y = state["snake"][0]
    if state["direction"] == "UP":
        new_head = (x, y - cell_size)
    elif state["direction"] == "DOWN":
        new_head = (x, y + cell_size)
    elif state["direction"] == "LEFT":
        new_head = (x - cell_size, y)
    elif state["direction"] == "RIGHT":
        new_head = (x + cell_size, y)
    state["snake"].insert(0, new_head)

# Draw replay button
def draw_replay_button():
    pygame.draw.rect(screen, gray, [screen_width // 2 - 75, screen_height // 2 + 50, 150, 50])
    font = pygame.font.SysFont(None, 36)
    text = font.render("Replay", True, black)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 60))

# Check if click is on replay button
def is_click_on_replay(pos):
    x, y = pos
    return screen_width // 2 - 75 <= x <= screen_width // 2 + 75 and screen_height // 2 + 50 <= y <= screen_height // 2 + 100

# Start game
state = init_game()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN and not state["game_over"]:
            if event.key == pygame.K_UP and state["direction"] != "DOWN":
                state["direction"] = "UP"
                change_color(state)
            elif event.key == pygame.K_DOWN and state["direction"] != "UP":
                state["direction"] = "DOWN"
                change_color(state)
            elif event.key == pygame.K_LEFT and state["direction"] != "RIGHT":
                state["direction"] = "LEFT"
                change_color(state)
            elif event.key == pygame.K_RIGHT and state["direction"] != "LEFT":
                state["direction"] = "RIGHT"
                change_color(state)

        elif event.type == pygame.MOUSEBUTTONDOWN and state["game_over"]:
            if is_click_on_replay(event.pos):
                state = init_game()

    if not state["game_over"]:
        move_snake(state)

        # Check collisions
        head_x, head_y = state["snake"][0]
        if head_x < 20 or head_x >= screen_width - 20 or head_y < 20 or head_y >= screen_height - 20:
            state["game_over"] = True
        if state["snake"][0] in state["snake"][1:]:
            state["game_over"] = True

        # Check food
        if state["snake"][0] == state["food"]:
            state["score"] += 1
            state["food"] = spawn_food()
        else:
            state["snake"].pop()

    # Draw screen
    screen.fill(black)

    # Walls
    pygame.draw.rect(screen, blue, [0, 0, screen_width, 20])
    pygame.draw.rect(screen, blue, [0, screen_height - 20, screen_width, 20])
    pygame.draw.rect(screen, blue, [0, 0, 20, screen_height])
    pygame.draw.rect(screen, blue, [screen_width - 20, 0, 20, screen_height])

    # Snake
    for part in state["snake"]:
        pygame.draw.rect(screen, state["color"], (part[0], part[1], cell_size, cell_size))

    # Food
    pygame.draw.rect(screen, red, (state["food"][0], state["food"][1], cell_size, cell_size))

    # Score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {state['score']}", True, white)
    screen.blit(score_text, (30, 30))

    # Game over text & replay
    if state["game_over"]:
        font_big = pygame.font.SysFont(None, 72)
        game_over_text = font_big.render("Game Over", True, red)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
        draw_replay_button()

    pygame.display.flip()
    clock.tick(10)
