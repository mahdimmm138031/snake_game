import pygame
import random

pygame.init()

# --- Game Settings ---
swidth, sheight = 820, 820
square_size = 40
cols = rows = (swidth - 20) // square_size
grid_offset = 10

screen = pygame.display.set_mode((swidth, sheight))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48)

MOVE = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE, 250)  # Set the movement speed to 250ms

# --- Game State ---
def reset_game():
    return {
        "running": True,
        "started": False,
        "direction": "right",
        "body": [(0, 0), (1, 0), (2, 0)],
        "food": None,
        "score": 0,
        "game_over": False
    }

game = reset_game()
high_score = 0

# --- Classes ---
class SnakeBlock:
    def __init__(self, color, x, y, size):
        self.color = color
        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

def spawn_food(body):
    while True:
        x = random.randint(0, cols - 1)
        y = random.randint(0, rows - 1)
        if (x, y) not in body:
            return (x, y)

# --- Main Game Loop ---
running = True
while running:
    screen.fill("white")

    # Draw Grid
    for i in range(cols + 1):
        pygame.draw.line(screen, (200, 200, 200), (grid_offset + i * square_size, grid_offset), (grid_offset + i * square_size, grid_offset + rows * square_size), 1)
    for j in range(rows + 1):
        pygame.draw.line(screen, (200, 200, 200), (grid_offset, grid_offset + j * square_size), (grid_offset + cols * square_size, grid_offset + j * square_size), 1)

    # Draw Food
    if game["food"]:
        fx, fy = game["food"]
        block_size = 30
        offset = (square_size - block_size) // 2
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            pygame.Rect(
                grid_offset + fx * square_size + offset,
                grid_offset + fy * square_size + offset,
                block_size,
                block_size
            )
        )

    # Draw Snake
    for index, (x, y) in enumerate(game["body"]):
        block_size = 30
        offset = (square_size - block_size) // 2
        screen_x = grid_offset + x * square_size + offset
        screen_y = grid_offset + y * square_size + offset

        # Head, Body, Tail colors
        if index == len(game["body"]) - 1:
            color = (0, 100, 0)  # Head
        elif index == 0:
            color = (100, 255, 100)  # Tail
        else:
            color = (0, 200, 0)  # Body

        SnakeBlock(color, screen_x, screen_y, block_size).draw(screen)

    # Draw Score
    score_text = font.render(f"Score: {game['score']}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (20, 10))
    screen.blit(high_score_text, (swidth - 200, 10))

    # Game Not Started
    if not game["started"] and not game["game_over"]:
        start_text = big_font.render("Press arrow key to start", True, (100, 100, 100))
        screen.blit(start_text, start_text.get_rect(center=(swidth // 2, sheight // 2)))

    # Game Over
    if game["game_over"]:
        over_text = big_font.render("Game Over!", True, (200, 0, 0))
        restart_text = font.render("Press R to restart", True, (0, 0, 0))
        screen.blit(over_text, over_text.get_rect(center=(swidth // 2, sheight // 2 - 40)))
        screen.blit(restart_text, restart_text.get_rect(center=(swidth // 2, sheight // 2 + 20)))

    pygame.display.flip()

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == MOVE and game["started"] and not game["game_over"]:
            head_x, head_y = game["body"][-1]

            if game["direction"] == "right":
                new_head = (head_x + 1, head_y)
            elif game["direction"] == "left":
                new_head = (head_x - 1, head_y)
            elif game["direction"] == "up":
                new_head = (head_x, head_y - 1)
            elif game["direction"] == "down":
                new_head = (head_x, head_y + 1)

            # Collision detection
            if (
                new_head in game["body"]
                or not (0 <= new_head[0] < cols)
                or not (0 <= new_head[1] < rows)
            ):
                game["game_over"] = True
                high_score = max(high_score, game["score"])
                continue

            game["body"].append(new_head)

            # Food eaten
            if game["food"] and new_head == game["food"]:
                game["score"] += 1
                game["food"] = spawn_food(game["body"])
            else:
                game["body"].pop(0)

        if event.type == pygame.KEYDOWN:
            if not game["started"] and not game["game_over"]:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    game["started"] = True
                    game["food"] = spawn_food(game["body"])

            if game["started"] and not game["game_over"]:
                if event.key == pygame.K_LEFT and game["direction"] != "right":
                    game["direction"] = "left"
                elif event.key == pygame.K_RIGHT and game["direction"] != "left":
                    game["direction"] = "right"
                elif event.key == pygame.K_UP and game["direction"] != "down":
                    game["direction"] = "up"
                elif event.key == pygame.K_DOWN and game["direction"] != "up":
                    game["direction"] = "down"

            # Restart
            if game["game_over"] and event.key == pygame.K_r:
                game = reset_game()

    clock.tick(60)

pygame.quit()
