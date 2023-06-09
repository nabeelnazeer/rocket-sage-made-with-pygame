import pygame
import os
pygame.font.init()

# Initialize Pygame
pygame.init()

# Set up the display window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Saga")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# setting fonts

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Define custom events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Set up the game clock
FPS = 60

# Set up the movement speed of the spaceships and bullets
VEL = 5
BULLETS_VEL = 7

# Set up the dimensions of the spaceships and the border between them
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Set up lists to hold the bullets for each spaceship

MAX_BULLETS =  10



# Load the images for the spaceships
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# background
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, RED_HEALTH, YELLOW_HEALTH):
    # Draw the game window
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_txt = HEALTH_FONT.render("Health : " + str(RED_HEALTH), 1, WHITE)
    yellow_health_txt = HEALTH_FONT.render("Health : " + str(YELLOW_HEALTH), 1, WHITE)

    WIN.blit(red_health_txt, (10,10))
    WIN.blit(yellow_health_txt, (WIDTH - yellow_health_txt.get_width()-10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Draw the bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # Update the display
    pygame.display.update()

def red_movement(keys_pressed, red):
    # Move the red spaceship
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL + red.width < BORDER.x:
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL + red.height < HEIGHT:
        red.y += VEL

def yellow_movement(keys_pressed, yellow):
    # Move the yellow spaceship
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > BORDER.x:
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x + VEL + yellow.width < WIDTH:
        yellow.x += VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y + VEL + yellow.height < HEIGHT:
        yellow.y += VEL
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in red_bullets:
        bullet.x += BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

def draw_winner(text):
    draw_txt = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_txt, (WIDTH/2 - draw_txt,get_width()/2, HEIGHT/2 - draw_txt.get_height()/2 ))
    pygame.display.update()
    pygame.time.delay(5000)

 
def main():
    red = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow =pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    # setting health
    RED_HEALTH = 10
    YELLOW_HEALTH =10

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_q and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5 )
                    red_bullets.append(bullet)

                if event.key == pygame.K_l and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5 )
                    yellow_bullets.append(bullet)
            if event.type == RED_HIT:
                RED_HEALTH -= 1



            if event.type == YELLOW_HIT:
                YELLOW_HEALTH -= 1
        winner_txt = ''
        if YELLOW_HEALTH <= 0:
            winner_txt = "Red won!"

        if RED_HEALTH <= 0:
            winner_txt =  "Yellow won!"

        if winner_txt != '':
            draw_winner(winner_txt)
            break       
        
        keys_pressed = pygame.key.get_pressed()
        red_movement(keys_pressed, red)
        yellow_movement(keys_pressed, yellow) 

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red ,yellow, red_bullets, yellow_bullets, RED_HEALTH, YELLOW_HEALTH)   

if __name__ == "__main__":
    main()

