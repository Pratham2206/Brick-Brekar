import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors (RGB values)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 204, 0)
blue = (0, 0, 255)
colors = [(255, 0, 0), (0, 204, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]

# Ball dimensions and radius
ball_radius = 10

# Paddle dimensions
paddle_width = 100
paddle_height = 15

# Brick dimensions
brick_width = 60
brick_height = 30

# Screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Brick Breaker')

# Function to create bricks
def create_bricks():
    bricks = []
    rows = 5  # Number of rows of bricks
    cols = 13  # Number of columns of bricks
    for row in range(rows):
        for col in range(cols):
            # Calculate brick position
            brick_x = col * (brick_width + 5) + 35
            brick_y = row * (brick_height + 5) + 35
            # Assign a random color to the brick
            brick_color = random.choice(colors)
            # Create brick as a rectangle and add to the list with its color
            bricks.append((pygame.Rect(brick_x, brick_y, brick_width, brick_height), brick_color))
    return bricks

# Function to draw bricks
def draw_bricks(bricks):
    for brick, color in bricks:
        # Draw each brick with its assigned color
        pygame.draw.rect(screen, color, brick)

# Function to draw the ball
def draw_ball(x, y):
    # Draw the ball as a white circle
    pygame.draw.circle(screen, white, (x, y), ball_radius)

# Function to draw the paddle
def draw_paddle(x, y):
    # Draw the paddle as a blue rectangle
    pygame.draw.rect(screen, blue, [x, y, paddle_width, paddle_height])

# Function to display text on the screen
def show_text(text, size, color, pos):
    # Set font and size
    font = pygame.font.SysFont("comicsansms", size)
    # Render the text
    render_text = font.render(text, True, color)
    # Blit the text to the screen
    screen.blit(render_text, pos)

# Main game loop
def game_loop():
    # Ball setup
    ball_x = screen_width // 2  # Ball starts in the middle of the screen
    ball_y = screen_height - paddle_height - ball_radius - 10  # Ball starts above the paddle
    ball_speed_x = 5 * random.choice((1, -1))  # Ball speed and direction
    ball_speed_y = -5  # Ball speed

    # Paddle setup
    paddle_x = screen_width // 2 - paddle_width // 2  # Paddle starts in the middle
    paddle_y = screen_height - paddle_height - 10  # Paddle position
    paddle_speed = 10  # Paddle speed

    # Brick setup
    bricks = create_bricks()  # Create initial bricks

    # Score setup
    score = 0  # Initial score

    # Lives setup
    lives = 3  # Initial lives

    # Main game loop
    running = True
    game_over = False
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit game
                running = False
                pygame.quit()
                return

        # Handle paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:  # Move paddle left
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:  # Move paddle right
            paddle_x += paddle_speed

        # Move the ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collision with top wall
        if ball_y - ball_radius <= 0:
            ball_speed_y *= -1

        # Ball collision with side walls
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
            ball_speed_x *= -1

        # Ball collision with bottom wall (lose a life)
        if ball_y + ball_radius >= screen_height:
            lives -= 1
            # Reset ball position and speed
            ball_x = screen_width // 2
            ball_y = screen_height - paddle_height - ball_radius - 10
            ball_speed_x = 5 * random.choice((1, -1))
            ball_speed_y = -5

        # Check for game over
        if lives == 0:
            game_over = True
            running = False

        # Ball collision with paddle
        if paddle_x < ball_x < paddle_x + paddle_width and paddle_y < ball_y + ball_radius < paddle_y + paddle_height:
            ball_speed_y *= -1

        # Ball collision with bricks
        for brick, color in bricks[:]:
            if brick.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)):
                ball_speed_y *= -1
                bricks.remove((brick, color))  # Remove brick when hit
                score += 1  # Increase score
                break
                 
        # Check if all bricks are destroyed
        if not bricks:
            game_over = False
            running = False

        # Draw everything
        screen.fill(black)  # Clear screen
        draw_ball(ball_x, ball_y)  # Draw ball
        draw_paddle(paddle_x, paddle_y)  # Draw paddle
        draw_bricks(bricks)  # Draw bricks

        # Display score and lives
        show_text(f"Score: {score}", 35, white, [20, 20])
        show_text(f"Lives: {lives}", 35, white, [screen_width - 150, 20])

        # Update the display
        pygame.display.flip()
        pygame.time.Clock().tick(60)  # 60 frames per second

    return game_over

# Main function
def main():
    while True:
        game_over = game_loop()  # Run the game loop
        screen.fill(black)  # Clear screen
        if game_over:  # Display game over message
            show_text("Game Over!", 50, white, [screen_width // 2 - 100, screen_height // 2 - 50])
        else:  # Display win message
            show_text("You Win!", 50, white, [screen_width // 2 - 100, screen_height // 2 - 50])
        show_text("Press C to Play Again or Q to Quit", 35, white, [screen_width // 2 - 200, screen_height // 2])
        pygame.display.flip()  # Update display
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit game
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Quit game
                        pygame.quit()
                        return
                    if event.key == pygame.K_c:  # Restart game
                        waiting = False

# Run the game
if __name__ == "__main__":
    main()
