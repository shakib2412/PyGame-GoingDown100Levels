import pgzrun
import random
import math

# Screen dimensions
WIDTH = 600
HEIGHT = 800

# Game parameters
PLAYER_SPEED = 4
BRICK_SPEED = 1.5
score = 0
high_score = 0
game_state = "intro"  # intro, playing, game_over
last_player_y = 0
animation_timer = 0

# Jump parameters
JUMP_SPEED = -12
GRAVITY = 0.5
player_velocity_y = 0
is_jumping = False

# Colors for UI and effects
COLORS = {
    'background': (15, 15, 35),  # Darker blue background
    'stars': [(255, 255, 255), (200, 200, 200), (150, 150, 150)],
    'score': (255, 223, 89),  # Golden yellow
    'title': (89, 216, 255),  # Light blue
    'text': (255, 255, 255),
    'game_over': (255, 89, 89),  # Soft red
    'button': (89, 149, 255)  # Button blue
}

# Initialize stars with different sizes
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT),
          random.choice(COLORS['stars']), random.uniform(0.5, 2))
         for _ in range(70)]


def reset_game():
    global player, bricks, score, player_velocity_y, is_jumping, game_state, last_player_y
    player = Actor('alien')
    player.x = WIDTH / 2
    player.y = HEIGHT / 5
    last_player_y = player.y

    bricks = []
    for i in range(6):
        brick = Actor('brick')
        brick.pos = 100 * (i + 1), 120 * (i + 1)
        bricks.append(brick)

    score = 0
    player_velocity_y = 0
    is_jumping = False
    game_state = "playing"


# Initialize game
reset_game()
game_state = "intro"  # Set back to intro


def draw_button(text, center_pos, selected=False):
    """Draw a stylized button with hover effect"""
    button_width = 200
    button_height = 40
    x = center_pos[0] - button_width // 2
    y = center_pos[1] - button_height // 2

    # Draw button background
    if selected:
        color = COLORS['button']
        text_color = COLORS['text']
    else:
        color = (COLORS['button'][0] // 2, COLORS['button'][1] // 2, COLORS['button'][2] // 2)
        text_color = COLORS['text']

    screen.draw.filled_rect(Rect((x, y), (button_width, button_height)), color)
    screen.draw.rect(Rect((x, y), (button_width, button_height)), COLORS['text'])
    screen.draw.text(text, center=center_pos, fontsize=20, color=text_color)


def draw():
    global animation_timer
    animation_timer += 1

    # Draw background
    screen.fill(COLORS['background'])

    # Draw animated stars
    for x, y, color, size in stars:
        # Add twinkling effect
        brightness = abs(math.sin(animation_timer * 0.05 + x * y)) * 0.3 + 0.7
        star_color = tuple(int(c * brightness) for c in color)
        screen.draw.filled_circle((x, y), size, star_color)

    if game_state == "intro":
        # Draw animated title
        title_y = HEIGHT / 4 + math.sin(animation_timer * 0.05) * 10
        screen.draw.text("ALIEN", center=(WIDTH / 2, title_y),
                         fontsize=80, color=COLORS['title'], shadow=(2, 2))
        screen.draw.text("PLATFORM", center=(WIDTH / 2, title_y + 70),
                         fontsize=60, color=COLORS['score'], shadow=(2, 2))

        # Draw animated instruction
        alpha = abs(math.sin(animation_timer * 0.05)) * 255
        instruction_color = (255, 255, 255, int(alpha))
        screen.draw.text("Press ENTER to Start",
                         center=(WIDTH / 2, HEIGHT * 2 / 3),
                         fontsize=30, color=instruction_color)

        screen.draw.text(f"High Score: {high_score}",
                         center=(WIDTH / 2, HEIGHT * 2 / 3 + 50),
                         fontsize=25, color=COLORS['text'])

    elif game_state == "playing":
        for brick in bricks:
            brick.draw()
        player.draw()

        # Draw score with style
        score_text = f"Score: {score}"
        screen.draw.text(score_text, (30, 20),
                         fontsize=30, color=COLORS['score'], shadow=(1, 1))
        screen.draw.text(f"High Score: {high_score}", (30, 50),
                         fontsize=20, color=COLORS['text'])

    elif game_state == "game_over":
        # Draw game world in background
        for brick in bricks:
            brick.draw()
        player.draw()

        # Draw semi-transparent overlay
        overlay = Rect((0, 0), (WIDTH, HEIGHT))
        screen.draw.filled_rect(overlay, (0, 0, 0, 180))

        # Draw game over text with animation
        title_y = HEIGHT / 3 + math.sin(animation_timer * 0.05) * 5
        screen.draw.text("GAME OVER", center=(WIDTH / 2, title_y),
                         fontsize=70, color=COLORS['game_over'], shadow=(3, 3))

        # Draw score panel
        panel_rect = Rect((WIDTH / 4, HEIGHT / 2 - 60), (WIDTH / 2, 120))
        screen.draw.filled_rect(panel_rect, (30, 30, 50, 200))
        screen.draw.rect(panel_rect, COLORS['text'])

        screen.draw.text(f"Final Score: {score}",
                         center=(WIDTH / 2, HEIGHT / 2 - 30),
                         fontsize=40, color=COLORS['score'])

        if score >= high_score and score > 0:
            screen.draw.text("New High Score!",
                             center=(WIDTH / 2, HEIGHT / 2 + 10),
                             fontsize=30, color=COLORS['title'])
        else:
            screen.draw.text(f"High Score: {high_score}",
                             center=(WIDTH / 2, HEIGHT / 2 + 10),
                             fontsize=30, color=COLORS['text'])

        # Draw buttons
        draw_button("Press ENTER to Restart",
                    (WIDTH / 2, HEIGHT * 2 / 3 + 20),
                    selected=True)
        draw_button("Press ESC to Exit",
                    (WIDTH / 2, HEIGHT * 2 / 3 + 70),
                    selected=False)


def update():
    global score, high_score, player_velocity_y, is_jumping, game_state, stars, last_player_y

    # Update star positions with different speeds based on size
    for i, (x, y, color, size) in enumerate(stars):
        new_y = (y + 0.2 * size) % HEIGHT
        stars[i] = (x, new_y, color, size)

    if game_state == "intro":
        if keyboard.RETURN:
            reset_game()

    elif game_state == "playing":
        player_on_ground = False

        for brick in bricks:
            if abs(player.bottom - brick.top) < 10 and \
                    abs(player.centerx - brick.centerx) < brick.width // 2:
                player.image = 'alien'
                player_on_ground = True
                player.bottom = brick.top
                player_velocity_y = 0
                is_jumping = False

                if last_player_y < brick.top:
                    score += 1
                    if score > high_score:
                        high_score = score

        last_player_y = player.y

        if keyboard.space and not is_jumping and player_on_ground:
            player_velocity_y = JUMP_SPEED
            is_jumping = True

        player_velocity_y += GRAVITY
        player_velocity_y = min(player_velocity_y, 10)
        player.y += player_velocity_y

        if keyboard.left:
            player.x = max(player.width // 2, player.x - PLAYER_SPEED)
        if keyboard.right:
            player.x = min(WIDTH - player.width // 2, player.x + PLAYER_SPEED)

        if not player_on_ground:
            player.image = 'alien_falling'

        for brick in bricks:
            brick.y -= BRICK_SPEED

        if bricks[0].top < 10:
            del bricks[0]
            new_brick = Actor('brick')
            new_brick.x = random.randint(player.width, WIDTH - player.width)
            new_brick.y = HEIGHT
            bricks.append(new_brick)

        if player.top < 0 or player.bottom > HEIGHT:
            game_state = "game_over"

    elif game_state == "game_over":
        if keyboard.RETURN:
            reset_game()
        elif keyboard.escape:
            exit()


pgzrun.go()