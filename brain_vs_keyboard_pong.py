import pygame
import sys
import keras
from EEGUtils import TestClassifier


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 10

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle positions
left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball position and speed
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x = 5
ball_speed_y = 5

model = keras.models.load_model("model.keras")
test_utils = TestClassifier(model, context_length=model.input_shape[1], num_classes=3)

# Game loop

test_utils.initialize_loop()
while True:
    test_utils.main_loop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Paddle movement
    keys = pygame.key.get_pressed()
    #if keys[pygame.K_w] and left_paddle.top > 0:
    #    left_paddle.y -= 5
    #if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
    #    left_paddle.y += 5
    #if keys[pygame.K_UP] and right_paddle.top > 0:
    #    right_paddle.y -= 5
    #if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
    #    right_paddle.y += 5

    if test_utils.last_predicted[0] > 1 and left_paddle.top > 0:
        left_paddle.y -= 5


    elif test_utils.last_predicted[1] and left_paddle.botom < HEIGHT:
        left_paddle.y += 5

    else:
      pass

    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= 5
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += 5


    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x = -ball_speed_x

    # Reset ball if it goes off screen
    if ball.left <= 0 or ball.right >= WIDTH:
        ball.x = WIDTH // 2
        ball.y = HEIGHT // 2
        ball_speed_x = -ball_speed_x  # Change direction

    # Clear screen
    screen.fill(BLACK)
   
    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Refresh the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Frame rate
