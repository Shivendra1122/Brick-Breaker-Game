import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker - Multi-colored Bricks")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)
CYAN = (0, 255, 255)

colors = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN, WHITE]

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Paddle
paddle_width, paddle_height = 100, 10
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 30, paddle_width, paddle_height)
paddle_speed = 7

# Ball
ball_radius = 8
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_radius * 2, ball_radius * 2)
ball_dx, ball_dy = 4, -4

# Bricks
brick_rows, brick_cols = 8, 10
brick_width, brick_height = WIDTH // brick_cols, 25
bricks = []

# Assign different colors to every brick
for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = col * brick_width
        brick_y = row * brick_height + 50
        brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        color = colors[(row * brick_cols + col) % len(colors)]  # cycle through colors
        bricks.append((brick, color))

# Score and lives
score = 0
lives = 3
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48)

game_over = False
game_win = False


def reset_ball():
    """Reset ball position to center."""
    global ball, ball_dx, ball_dy
    ball.x, ball.y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = 4, -4


def draw():
    screen.fill(BLACK)
    # Draw paddle
    pygame.draw.rect(screen, GREEN, paddle)
    # Draw ball
    pygame.draw.circle(screen, WHITE, (ball.x + ball_radius, ball.y + ball_radius), ball_radius)
    # Draw bricks
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick)
    # HUD
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))

    # Win/Lose messages
    if game_over:
        text = big_font.render("YOU LOSE! GAME OVER", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    elif game_win:
        text = big_font.render("YOU WIN! BRICKS CLEARED!", True, YELLOW)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()


# Game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over and not game_win:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += paddle_speed

        # Ball movement
        ball.x += ball_dx
        ball.y += ball_dy

        # Collision with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_dx *= -1
        if ball.top <= 0:
            ball_dy *= -1

        # Collision with paddle
        if ball.colliderect(paddle):
            ball_dy *= -1

        # Collision with bricks
        hit_index = ball.collidelist([b[0] for b in bricks])
        if hit_index != -1:
            del bricks[hit_index]
            ball_dy *= -1
            score += 10

        # Check win
        if not bricks:
            game_win = True

        # Ball falls below screen
        if ball.bottom >= HEIGHT:
            lives -= 1
            if lives > 0:
                reset_ball()
            else:
                game_over = True

    draw()

pygame.quit()
sys.exit()