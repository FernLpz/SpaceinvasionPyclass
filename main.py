"""This is a game with """

import pygame
import random
import math

#initialize pygame
pygame.init()

#Create game screen
screen = pygame.display.set_mode((800, 600))

#set icon and title
pygame.display.set_caption("space Invaders")
ovni = pygame.image.load("ovni.png")
pygame.display.set_icon(ovni)
background = pygame.image.load("back.jpg")

#Player variables
img_player = pygame.image.load("astronave.png")
player_x = 368
player_y = 536
player_x_change = 0

#Bullet variables
img_Bullet = pygame.image.load("bullet.png")
Bullet_x = 0
Bullet_y = 536
Bullet_x_change = 0.5
Bullet_y_change = 0.5
bullet_visible = False

# Score Variables
Score = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)
score_text_x = 10
score_text_y = 10

#End game
end_font = pygame.font.Font("freesansbold.ttf", 64)

#End message
def final_message():
    final_text = end_font.render(f"GAME OVER : {Score}", True, (255, 255, 255))
    screen.blit(final_text, (200, 200))

#Enemy variables
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_enemys = 5

for i in range(number_enemys):
    img_enemy.append(pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(0, 200))
    enemy_x_change.append(0.3)
    enemy_y_change.append(30)

#show score
def show_score(x, y):
    text = score_font.render(f"Score: {Score}", True, (255, 255, 255))
    screen.blit(text, (x, y))

#Show player in screen
def player(x, y):
    screen.blit(img_player, (x, y))

def enemy(x, y, enemy_index):
    screen.blit(img_enemy[enemy_index], (x, y))

def shoot_bullet(x, y):
    global bullet_visible
    bullet_visible = True
    screen.blit(img_Bullet, (x + 16, y + 10))

def detect_collision (x_1, y_1, x_2, y_2):
    x_sub = x_2 - x_1
    y_sub = y_2 - y_1
    dist = math.sqrt(math.pow(x_sub, 2) + math.pow(y_sub, 2))
    if dist < 27:
        return True
    else:
        return False


#Game loop
is_running = True
while is_running:
    #RGB Background
    #screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))


    #player_x+= 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            print("A key was press")
            if event.key == pygame.K_LEFT: #if left arrow is pressed
                print("Left arrow pressed")
                player_x_change -= 1
            if event.key == pygame.K_RIGHT:
                print("RIGHT arrow pressed")
                player_x_change += 1
            if event.key == pygame.K_SPACE:
                if not bullet_visible:
                    Bullet_x = player_x
                    shoot_bullet(player_x, Bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("Arrow keys were release")
                player_x_change = 0

    #update player location
    player_x += player_x_change

    # keep player inside the screen
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(number_enemys):
        #End game
        if enemy_y[i] > 450:
            for j in range(number_enemys):
                enemy_y[j] = 1000
            final_message()
            break


        #update enemy location
        enemy_x[i] += enemy_x_change[i]

        # keep enemy inside the screen
        if enemy_x[i] <= 0:
            enemy_x_change[i] += 0.7
            enemy_y[i] += enemy_x_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] -= 0.7
            enemy_y[i] += enemy_y_change[i]

        #Detect colission
        collision = detect_collision(enemy_x[i], enemy_y[i], Bullet_x, Bullet_y)
        if collision:
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(30, 200)
            bullet_visible = False
            Score += 1
            Bullet_y = 500
            print(Score)

        # show enemy
        enemy(enemy_x[i], enemy_y[i], i)


    # Shoot Bullet
    if Bullet_y <= 64:
        Bullet_y = 500
        bullet_visible = False
    if bullet_visible:
        shoot_bullet(Bullet_x, Bullet_y)
        Bullet_y -= Bullet_y_change

    #Show player
    player(player_x, player_y)

    #show score
    show_score(score_text_x, score_text_y)

    #Update game
    pygame.display.update()
