import pygame
from pygame import mixer
import os

pygame.init() # initialise pygame
pygame.font.init() # initialise python font library
mixer.init() # initialise mixer

# setup
WIDTH, HEIGHT = 1200, 675
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) # WIN is the window it will be displayed
pygame.display.set_caption('Shootout.py')
FPS = 60 # Frames per second
VEL = 15 # velocity 
BULLETSVEL = 30 # bullets velocity
MAXBULLETS = 4
HEALTH_FONT = pygame.font.SysFont('comicsans', 25)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# set events
p1hit = pygame.USEREVENT + 1
p2hit = pygame.USEREVENT + 2

# sound
gunshot = pygame.mixer.Sound(os.path.join('assets', 'Gunshot.m4a')) # sound effects
bgsong = mixer.music.load(os.path.join('assets', 'SouthParkTheme.m4a')) # load music
mixer.music.set_volume(0.7)
mixer.music.play(-1) # -1 to not stop playing music (infinite loop)

#border
top = 0
bottom = 675
leftborder = 0
rightborder = 1200

# render in images and change background
WHITE = (255, 255, 255) # set colours by RGB
RED = (255,0,0)
BLUE = (0,0,255)

player1 = pygame.image.load(os.path.join('assets', 'Kyle.jpg')) # upload images
player2 = pygame.image.load(os.path.join('assets', 'Eric.jpg'))
arena = pygame.image.load(os.path.join('assets', 'Arena.jpg'))

# size of characters
# player 1
player1length = 73
player1tall = 90
# player 2
player2length = 73
player2tall = 90

# placement
arena_width, arena_height = 0, 0
player1_width, player1_height = 311, HEIGHT/2 - player1tall/2
player2_width, player2_height = WIDTH - 311 - player2length, HEIGHT/2 - player2tall/2
      
# display
def draw_window(p1, p2, p1bullets, p2bullets, p1_health, p2_health): 
    WIN.fill(WHITE) # set colour of window background to white
    WIN.blit(arena, (arena_width, arena_height)) # set background image

    # health bars
    p1_healthbar = HEALTH_FONT.render(f'Player 1 Health: {str(p1_health)}', 1, WHITE) 
    p2_healthbar = HEALTH_FONT.render(f'Player 2 Health: {str(p2_health)}', 1, WHITE) 
    WIN.blit(p1_healthbar, (20,HEIGHT - p1_healthbar.get_height() - 20)) # add health bars
    WIN.blit(p2_healthbar, (WIDTH - p2_healthbar.get_width() - 20, HEIGHT - p2_healthbar.get_height() - 20))

    # add sprites
    WIN.blit(player1, (p2.x, p2.y)) 
    WIN.blit(player2, (p1.x, p1.y))

    # draw bullets
    for bullet in p1bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in p2bullets:
        pygame.draw.rect(WIN, BLUE, bullet)
          
    pygame.display.update()

# movement functions
# player 1
def player1_movement(keys_pressed, p1):
    if keys_pressed[pygame.K_w] and p1.y > top: # up for player 1   
        p1.y -= VEL
    if keys_pressed[pygame.K_s] and p1.y < bottom - player1tall: # down for player 1 
        p1.y += VEL
    if keys_pressed[pygame.K_a] and p1.x > leftborder: # left for player 1
        p1.x -= VEL
    if keys_pressed[pygame.K_d] and p1.x < rightborder/2 - player1length*1.5: # right for player 1
        p1.x += VEL

# player 2
def player2_movement(keys_pressed, p2):
    if keys_pressed[pygame.K_UP] and p2.y > top: # up for player 2
        p2.y -= VEL 
    if keys_pressed[pygame.K_DOWN] and p2.y < bottom - player2tall: # down for player 2    
        p2.y += VEL
    if keys_pressed[pygame.K_LEFT] and p2.x > (rightborder/2) : # left for player 2   
        p2.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and p2.x < rightborder - player2length: # right for player 2
        p2.x += VEL

# bullet handling
def bulletmovement(p1bullets, p2bullets, p1, p2):
    for p1bullet in p1bullets:      
        p1bullet.x += BULLETSVEL # moves bullet to right
        if p2.colliderect(p1bullet):
            pygame.event.post(pygame.event.Event(p2hit)) # event to main function for collision
            p1bullets.remove(p1bullet)
        elif p1bullet.x >=  WIDTH:
            p1bullets.remove(p1bullet)

    for p2bullet in p2bullets:
        p2bullet.x -= BULLETSVEL # moves bullet to left
        if p1.colliderect(p2bullet):
            pygame.event.post(pygame.event.Event(p1hit))
            p2bullets.remove(p2bullet)
        elif p2bullet.x <= 0:
            p2bullets.remove(p2bullet)
      
# display winner message
def winner(winner_text):
    draw_winner_text = WINNER_FONT.render(winner_text, 1 , WHITE)
    WIN.blit(draw_winner_text, (WIDTH/2 - draw_winner_text.get_width()/2, HEIGHT/2 - draw_winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    main()

# run the game
def main():
    run = True # if true, game will run

    p1 = pygame.Rect(player1_width, player1_height, player1length, player1tall)
    p2 = pygame.Rect(player2_width, player2_height, player2length, player2tall)

    p1bullets = []
    p2bullets = []
    p1_health = 5
    p2_health = 5

    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # user quitting will be detected
                run = False
                pygame.quit()

            # bullet controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and len(p1bullets) < MAXBULLETS: # p1 bullets
                    p1bullet = pygame.Rect(p1.x + 40, p1.y + 20 + player1tall//2, 15, 10) # position and size of bullets
                    gunshot.play()
                    p1bullets.append(p1bullet)
                    
                if event.key == pygame.K_BACKSLASH and len(p2bullets) < MAXBULLETS: # p2 bullets 
                    p2bullet = pygame.Rect(p2.x, p2.y + player2tall//2 , 15, 10)
                    gunshot.play()
                    p2bullets.append(p2bullet)

            # handling player health 
            if event.type == p1hit:
                p1_health -= 1

            if event.type == p2hit:
                p2_health -= 1

        # declaring winner
        winner_text = ''

        if p1_health <= 0:
            winner_text = 'Player 2 wins!'
        
        if p2_health <= 0:
            winner_text = 'Player 1 wins!'

        if winner_text != '':
            winner(winner_text)
        
        keys_pressed = pygame.key.get_pressed()
        player1_movement(keys_pressed, p1) # p1 for player 1
        player2_movement(keys_pressed, p2) # p2 for player 2
        bulletmovement(p1bullets, p2bullets, p1, p2)

        draw_window(p1, p2, p1bullets, p2bullets, p1_health, p2_health)# background will keep running 

if __name__ == '__main__':
    main()