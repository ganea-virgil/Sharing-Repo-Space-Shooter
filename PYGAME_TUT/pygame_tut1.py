# Pygame in 90 Minutes - For Beginners
# Left at 1:30:00

# Avoid hardcoding at all costs!!! Use variables and math operations to get what I need!

# Add rounds won counter
# Add really simple menu

### Improvements

# Add random movement(just change the x and y coordinates randomly) to
# the red ship to create a basic AI !!! Maybe even increase red ship velocity(speed, 
# add a new constant ENEMY_VEL)!
# !!! Create a separate version with red ship as AI !!!

import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720    # Yes, I can initialize variables one after the other
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2P Space Shooter')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 75, 0)
BLUE = (0, 0, 255)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun.ogg"))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade.ogg'))
NEW_ROUND_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'mixkit-retro-game-notification-212.ogg'))
pygame.mixer.music.load(os.path.join('Assets', 'A Soul as Red as a Ground Cherry.ogg'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 50)
WINNER_FONT = pygame.font.SysFont('comicsans', 120)

FPS = 60
VEL = 7  # Velocity(Speed of Spaceship in pixels per frame)
BULLET_VEL = 10
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 60      # in pixels

YELLOW_HIT = pygame.USEREVENT + 1   # USEREVENT is a number, we add 1 to them to make sure we have a unique event number
RED_HIT = pygame.USEREVENT + 2


YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))    # Nested methods; 2 lines in 1

pygame.mixer.music.play(-1)


def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):
    # WIN.fill(WHITE)   # For testing
    WIN.blit(BACKGROUND, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    yellow_health_text = HEALTH_FONT.render(f"Health:{str(yellow_health)}", 1, WHITE)
    red_health_text = HEALTH_FONT.render(f"Health:{str(red_health)}", 1, WHITE)
    WIN.blit(yellow_health_text, (0 + 10, 0 + 5))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 0 + 5))


    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))      # Top left corner drawing position
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, WHITE, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, WHITE, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and (yellow.x + yellow.width) + VEL < BORDER.x: # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and (yellow.y + yellow.height) + VEL < HEIGHT: # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and (red.x + red.width) + VEL < WIDTH: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and (red.y + red.height) + VEL < HEIGHT: # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x + bullet.width < 0:
            red_bullets.remove(bullet)


def draw_winner(winner_text):
    if winner_text == "Red Wins!":
        winner_message = WINNER_FONT.render(winner_text, 1, RED)
    else:
        winner_message = WINNER_FONT.render(winner_text, 1, YELLOW)
    WIN.blit(winner_message, (WIDTH // 2 - winner_message.get_width() // 2, HEIGHT // 2 - winner_message.get_height() // 2))
    pygame.display.update()
    pygame.mixer.stop()
    pygame.time.delay(4000)     # in milliseconds(1000ms = 1sec)
    pygame.event.clear(eventtype=pygame.KEYDOWN)    # Prevents key buffer from bleeding into the next round
    NEW_ROUND_SOUND.play()



def main():
    # Since we have defined all the variables in this function,
    # when we call it again everything resets. We can restart the game safely
    yellow = pygame.Rect(WIDTH//4 - SPACESHIP_WIDTH//2, HEIGHT//2 - SPACESHIP_HEIGHT//2, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)     # I swapped SPACESHIP_HEIGHT and height to compensate for the fact the we rotated the models 90 degrees. The image is tall and the rect is wide. That's why I need to swap width and height!
    red = pygame.Rect(WIDTH-WIDTH/4 - SPACESHIP_WIDTH//2, HEIGHT//2 - SPACESHIP_HEIGHT//2, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False     # I don't think there is a point to this since quit() ends the script
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 3, 13, 6)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x - 10, red.y + red.height // 2 - 3, 13, 6)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        elif red_health <= 0:               # Risk. I put elif instead of if 
            winner_text = "Yellow Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health)

    main()

if __name__ == "__main__":      # If we call the function directly then run main(). If it's imported in another script, main() won't run
    main()