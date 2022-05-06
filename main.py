import pygame
import math
import random
from pygame import mixer
pygame.init()

# display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Backgrround img

bg_img = pygame.image.load("images/bg_re.jpg")

# Background sound
mixer.music.load("music/background.wav")
mixer.music.play(-1)

# ADDING CAPTION
pygame.display.set_caption("Space Invaders")

# ADDING ICON FOR GAME
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

# player img
player_img = pygame.image.load("images/spaceship.png")
player_x = 380
player_y = 480
# this variable will be used to change the speed of the player
player_x_change = 0

# player img
# creating a list for multiple enemies
enemy_img =[]
enemy_x =[]
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append( pygame.image.load("images/ufo.png"))
    enemy_x.append(random.randint(0, screen_width - 64))
    enemy_y.append(random.randint(50, 150))
    # this variable will be used to change the speed of the player
    enemy_x_change.append( 0.2)
    enemy_y_change.append(30)

# for bullets
bullet_img = pygame.image.load("images/bullet.png")
bullet_x = 0
bullet_y = 480
# this variable will be used to change the speed of the player
bullet_x_change = 0
bullet_y_change = .5
# Ready state -> You cant see the bullet in the screen
# Fire state -> the bullet can be seen
bullet_state = "ready"
# this fuction display the img in the screen calling the blit() fun in the pygame module

# SCORE 
score_value = 0
font = pygame.font.Font("freesansbold.ttf",42)

text_x=10
text_y=10
def show_score(x,y):
    score = font.render("Score : " + str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))

# game over score
over_font = pygame.font.Font("freesansbold.ttf",62)
def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y,i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def iscollision(enemy_x,enemy_y,bullet_x,bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y,2))
    if distance < 27:
        return  True
    else: 
        return False


# game loop
running = True
while running:
    # screen rgb color its black
    screen.fill((0, 0, 0))
    # background image
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # IF KEYSTROKE IS PRESSED THEN MOVE
        if event.type == pygame.KEYDOWN:
            # print("A keystroke is pressed ")
            if event.key == pygame.K_LEFT:
                # print("left arrow is pressed")
                player_x_change = -0.3
            if event.key == pygame.K_RIGHT:
                # print("Right arrow is pressed")
                player_x_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound=mixer.Sound("G:\PYGAME\space_game\music/laser.wav")
                    bullet_sound.play()
                    bullet_x=player_x
                    fire_bullet(bullet_x,bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Keystroke has been released")
                player_x_change = 0

    # incrementing the change when the keys are pressed
    player_x += player_x_change

    # rectricting the player from going outside the screen
    if player_x <= 0:
        player_x = 0
    elif player_x >= screen_width - 64:
        player_x = screen_width - 64

    # for enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemy_y[i]>300:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.2
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= screen_width - 64:
            enemy_x_change[i] = - 0.2
            enemy_y[i] += enemy_y_change[i]

        # collision
        collision= iscollision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        if collision:
            explosion_sound=mixer.Sound("G:\PYGAME\space_game\music/explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            # print(score)
            enemy_x[i] = random.randint(0, screen_width - 64)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i],i)

    # Bullet movement
    if bullet_y<=0:
        bullet_y=480
        bullet_state="ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x,bullet_y)
        bullet_y -= bullet_y_change

     
    player(player_x, player_y)
    show_score(text_x,text_y)
    # updating the screen to show the changes
    pygame.display.update()
